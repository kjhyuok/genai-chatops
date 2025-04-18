import json
import logging
import os
import boto3
import botocore
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from datetime import datetime
from atlassian import Confluence
from botocore.exceptions import ClientError
import time
import hmac
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret(secret):
    secret_name = os.getenv('SLACK_TOKEN_SECRET')
    region_name = os.getenv('REGION')

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret_string = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret_string)

    return secret_dict[secret]

OAUTH_TOKEN = get_secret('slack_token')
WIKI_URL = get_secret('wiki_url')
WIKI_API_KEY = get_secret('wiki_api_key')
WIKI_USER = get_secret('wiki_user')
AGENT_ID = get_secret('bedrock_agent')
ALIAS_ID = get_secret('bedrock_agent_alias')

SLACK_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OAUTH_TOKEN}"
}
session = boto3.Session()
	
def get_user_name(user_id, user_name_cache):
    if user_id not in user_name_cache:
        response = requests.get(f"https://slack.com/api/users.info?user={user_id}", headers=SLACK_HEADERS)
        user_info = response.json()
        user_name_cache[user_id] = user_info.get("user", {}).get("name", user_id)
    return user_name_cache[user_id]

def send_slack_message(channel, text, thread_ts=None):
    message = {"channel": channel, "text": text, "thread_ts": thread_ts}
    requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json=message)

def create_confluence_page(content):
    confluence = Confluence(url=WIKI_URL, username=WIKI_USER, password=WIKI_API_KEY)
    response = confluence.create_page(
        space="issuehistory",
        title=f"slack reporting - {datetime.now().strftime('%Y.%m.%d %H:%M')}",
        body="(Amazon Bedrock에 의해 요약 작성된 내용입니다.)<br><br>" + content.replace("\n", "<br>"),
        parent_id="98657"
    )
    return response.get("id")

def invoke_bedrock_agent(input_text, analysis_type, session_id):
    print("session_id : ", session_id)
    prompts = {
        'analysis': "Please analyze the following error. All conversations should be in Korean: ",
        'summary': "Summarize the following conversation. This summary should include information about the cause and progress, solution, status, and relevant participants so that the issue can be reviewed later, and be in Korean in all languages.: "
    }
    client = session.client('bedrock-agent-runtime', region_name='us-west-2', config=botocore.config.Config(read_timeout=900, connect_timeout=900, retries={"max_attempts": 0}))
    try:
        response = client.invoke_agent(
            agentAliasId=ALIAS_ID,
            agentId=AGENT_ID,
            sessionId=session_id,
            inputText=prompts[analysis_type] + input_text
        )
        return ''.join(event["chunk"]["bytes"].decode() for event in response.get("completion", []))
    except Exception as e:
        logger.error(f"Error invoking Bedrock agent: {e}")
        return f"Error invoking Bedrock agent: {str(e)}"

def get_comments_thread(channel_id, thread_ts):
    response = requests.get("https://slack.com/api/conversations.replies", headers=SLACK_HEADERS, params={"channel": channel_id, "ts": thread_ts})
    replies = response.json().get("messages", [])
    user_name_cache = {}
    replies_text = "\n".join(
        f"{get_user_name(reply.get('user'), user_name_cache)}: {reply.get('text')}" for reply in replies if reply.get("text") and reply.get("user")
    )
    try:
        bedrock_response = invoke_bedrock_agent(replies_text, 'summary', thread_ts)
        page_id = create_confluence_page(bedrock_response)
        send_slack_message(channel_id, f"Report가 등록되었습니다.\n{WIKI_URL}/spaces/issuehistory/pages/{page_id}", thread_ts)
        return {"result": bedrock_response}
    except SlackApiError as e:
        logger.error(f"Slack API error: {e.response['error']}")
        return {"result": "Slack reply failed"}

def lambda_handler(event, context):
    print(event)
    bt_value = event['actions'][0]['value']
    thread_ts = event["message"]["ts"]
    channel_id = event["channel"]["id"]
    print("thread_ts : ", thread_ts)
    print("channel_id : ", channel_id)

    if bt_value == "click_watch":
        send_slack_message(channel_id, f"<@{event['user']['username']}> 님이 Watching 중 입니다.", thread_ts)
    elif bt_value == "click_agent":
        error_message = next(
            (block['text']['text'] for block in event["message"]["blocks"] if block.get('block_id') == 'error_text'), 
            None
        )
        send_slack_message(channel_id, f"저는 Error MSG를 전달하는 AWS ChatBot 입니다. ", thread_ts)
        send_slack_message(channel_id, f"<@q> ask 커넥터이름 "+"에게 이 오류에 대한 분석을 요청할게\n" + f"*MSG 원문*:\n{error_message}", thread_ts)
        send_slack_message(channel_id, "분석중이니 잠시만 기다려주세요.", thread_ts)        

    elif bt_value == "click_reporting":
        send_slack_message(channel_id, "Reporting 생성 중입니다. 잠시만 기다려주세요.", thread_ts)
        get_comments_thread(channel_id, thread_ts)
