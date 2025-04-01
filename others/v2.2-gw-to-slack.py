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

# def create_confluence_page(content, thread_ts):
#     try:
#         confluence = Confluence(url=WIKI_URL, username=WIKI_USER, password=WIKI_API_KEY)
        
#         # 현재 시간 포맷팅
#         current_time = datetime.now().strftime('%Y.%m.%d %H:%M')
        
#         # HTML 형식으로 내용 구성
#         html_content = f"""
#         <h2>장애 보고서 - {current_time}</h2>
#         <div class="content-wrapper">
#             <div class="metadata">
#                 <p><strong>작성일시:</strong> {current_time}</p>
#                 <p><strong>Thread ID:</strong> {thread_ts}</p>
#             </div>
#             <div class="summary">
#                 <h3>요약</h3>
#                 {content.replace("\n", "<br>")}
#             </div>
#         </div>
#         <p><em>※ 이 보고서는 Amazon Bedrock에 의해 자동 생성되었습니다.</em></p>
#         """

#         # Confluence 페이지 생성
#         response = confluence.create_page(
#             space="WinningGen",
#             title=f"Slack 장애 보고서 - {current_time}",
#             body=html_content,
#             parent_id="2129937"  # 지정된 parent_id 사용
#         )
        
#         return response.get("id")
#     except Exception as e:
#         logger.error(f"Error creating Confluence page: {str(e)}")
#         raise

def create_confluence_page(content, thread_ts):
    try:
        confluence = Confluence(url=WIKI_URL, username=WIKI_USER, password=WIKI_API_KEY)
        
        # 현재 시간 포맷팅
        current_time = datetime.now().strftime('%Y.%m.%d %H:%M')
        
        # 내용을 구조화된 형식으로 파싱
        try:
            content_lines = content.split('\n')
            parsed_content = {
                'cause': '',
                'progress': '',
                'solution': '',
                'status': '',
                'participants': ''
            }
            
            current_section = ''
            for line in content_lines:
                line = line.strip()
                if '원인:' in line or 'Cause:' in line:
                    current_section = 'cause'
                    parsed_content['cause'] = line.split(':', 1)[1].strip()
                elif '진행상황:' in line or 'Progress:' in line:
                    current_section = 'progress'
                    parsed_content['progress'] = line.split(':', 1)[1].strip()
                elif '해결방안:' in line or 'Solution:' in line:
                    current_section = 'solution'
                    parsed_content['solution'] = line.split(':', 1)[1].strip()
                elif '상태:' in line or 'Status:' in line:
                    current_section = 'status'
                    parsed_content['status'] = line.split(':', 1)[1].strip()
                elif '참여자:' in line or 'Participants:' in line:
                    current_section = 'participants'
                    parsed_content['participants'] = line.split(':', 1)[1].strip()
                elif line and current_section:
                    parsed_content[current_section] += ' ' + line
        except Exception as e:
            logger.warning(f"Content parsing error: {e}")
            parsed_content = {
                'cause': 'Parsing failed',
                'progress': content,
                'solution': '',
                'status': '',
                'participants': ''
            }

        # HTML 형식으로 내용 구성 (개선된 스타일)
        html_content = f"""
        <h1 style="color: #172b4d; font-family: Arial, sans-serif;">장애 보고서</h1>
        <div class="content-wrapper">
            <table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; border: 1px solid #dfe1e6;">
                <colgroup>
                    <col style="width: 15%;">
                    <col style="width: 85%;">
                </colgroup>
                <tbody>
                    <tr style="background-color: #f4f5f7;">
                        <th style="padding: 10px; border: 1px solid #dfe1e6; text-align: left; font-weight: bold;">작성일시</th>
                        <td style="padding: 10px; border: 1px solid #dfe1e6;">{current_time}</td>
                    </tr>
                    <tr>
                        <th style="padding: 10px; border: 1px solid #dfe1e6; text-align: left; font-weight: bold;">Thread ID</th>
                        <td style="padding: 10px; border: 1px solid #dfe1e6;">{thread_ts}</td>
                    </tr>
                    <tr style="background-color: #f4f5f7;">
                        <th style="padding: 10px; border: 1px solid #dfe1e6; text-align: left; font-weight: bold;">장애 원인</th>
                        <td style="padding: 10px; border: 1px solid #dfe1e6;">{parsed_content['cause']}</td>
                    </tr>
                    <tr>
                        <th style="padding: 10px; border: 1px solid #dfe1e6; text-align: left; font-weight: bold;">진행 상황</th>
                        <td style="padding: 10px; border: 1px solid #dfe1e6;">
                            <ac:structured-macro ac:name="expand">
                                <ac:parameter ac:name="title">진행 상황 상세보기</ac:parameter>
                                <ac:rich-text-body>
                                    <p>{parsed_content['progress'].replace('\n', '<br/>')}</p>
                                </ac:rich-text-body>
                            </ac:structured-macro>
                        </td>
                    </tr>
                    <tr style="background-color: #f4f5f7;">
                        <th style="padding: 10px; border: 1px solid #dfe1e6; text-align: left; font-weight: bold;">해결 방안</th>
                        <td style="padding: 10px; border: 1px solid #dfe1e6;">{parsed_content['solution']}</td>
                    </tr>
                    <tr>
                        <th style="padding: 10px; border: 1px solid #dfe1e6; text-align: left; font-weight: bold;">현재 상태</th>
                        <td style="padding: 10px; border: 1px solid #dfe1e6;">{parsed_content['status']}</td>
                    </tr>
                    <tr style="background-color: #f4f5f7;">
                        <th style="padding: 10px; border: 1px solid #dfe1e6; text-align: left; font-weight: bold;">참여자</th>
                        <td style="padding: 10px; border: 1px solid #dfe1e6;">{parsed_content['participants']}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <br/>
        <h2 style="color: #172b4d; font-family: Arial, sans-serif;">원본 내용</h2>
        <div class="raw-content">
            <ac:structured-macro ac:name="expand">
                <ac:parameter ac:name="title">전체 대화 내용 보기</ac:parameter>
                <ac:rich-text-body>
                    <ac:structured-macro ac:name="code">
                        <ac:parameter ac:name="language">none</ac:parameter>
                        <ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body>
                    </ac:structured-macro>
                </ac:rich-text-body>
            </ac:structured-macro>
        </div>
        <p style="font-style: italic; color: #5e6c84; font-size: 12px; font-family: Arial, sans-serif;">※ 이 보고서는 Amazon Bedrock에 의해 자동 생성되었습니다.</p>
        """

        # Confluence 페이지 생성
        response = confluence.create_page(
            space="WinningGen",
            title=f"Slack 장애 보고서 - {current_time}",
            body=html_content,
            parent_id="2129937"
        )
        
        return response.get("id")
    except Exception as e:
        logger.error(f"Error creating Confluence page: {str(e)}")
        raise

def get_comments_thread(channel_id, thread_ts):
    try:
        # Slack API를 통해 스레드의 모든 메시지 가져오기
        response = requests.get(
            "https://slack.com/api/conversations.replies",
            headers=SLACK_HEADERS,
            params={"channel": channel_id, "ts": thread_ts}
        )
        
        if not response.json().get("ok"):
            raise Exception("Failed to fetch thread messages")

        replies = response.json().get("messages", [])
        user_name_cache = {}
        
        # 대화 내용 구성
        replies_text = "\n".join(
            f"{get_user_name(reply.get('user'), user_name_cache)}: {reply.get('text')}"
            for reply in replies
            if reply.get("text") and reply.get("user")
        )

        # Bedrock Agent를 통한 요약 생성
        bedrock_response = invoke_bedrock_agent(replies_text, 'summary', thread_ts)
        
        # Confluence 페이지 생성
        page_id = create_confluence_page(bedrock_response, thread_ts)
        
        # 성공 메시지 전송
        confluence_link = f"{WIKI_URL}/pages/viewpage.action?pageId={page_id}"
        send_slack_message(
            channel_id,
            f":white_check_mark: 보고서가 성공적으로 생성되었습니다.\n"
            f"*링크*: {confluence_link}",
            thread_ts
        )
        
        return {"statusCode": 200, "body": json.dumps({"message": "Success"})}
        
    except Exception as e:
        error_msg = f"보고서 생성 중 오류가 발생했습니다: {str(e)}"
        logger.error(error_msg)
        send_slack_message(channel_id, f":x: {error_msg}", thread_ts)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def invoke_bedrock_agent(input_text, analysis_type, session_id):
    prompts = {
        'analysis': "Please analyze the following error. All conversations should be in Korean: ",
        'summary': """
        다음 대화를 분석하여 아래 형식으로 요약해주세요:

        원인: [문제의 근본 원인]
        진행상황: [문제 해결을 위해 수행된 작업들]
        해결방안: [제시된 또는 적용된 해결책]
        상태: [현재 문제 해결 상태]
        참여자: [대화에 참여한 주요 인원]
        """
    }
    client = session.client('bedrock-agent-runtime', region_name='ap-northeast-2', config=botocore.config.Config(read_timeout=900, connect_timeout=900, retries={"max_attempts": 0}))
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

def handle_expert_assignment(payload):
    """Expert 할당 모달 제출 처리"""
    try:
        metadata = json.loads(payload["view"]["private_metadata"])
        values = payload["view"]["state"]["values"]
        
        expert_user = values["expert_user"]["user_select"]["selected_user"]
        message_content = values["message_content"]["message_input"]["value"]
        
        channel_id = metadata["channel"]
        thread_ts = metadata["thread_ts"]
        requesting_user = payload["user"]["id"]

        # 현재 스레드의 원문 메시지 가져오기
        response = requests.get(
            f"https://slack.com/api/conversations.replies?channel={channel_id}&ts={thread_ts}",
            headers=SLACK_HEADERS
        )
        
        if not response.json().get("ok"):
            raise Exception("Failed to fetch thread messages")
        
        messages = response.json().get("messages", [])
        original_error = next(
            (msg["text"] for msg in messages if msg.get("ts") == thread_ts),
            "Original error message not found"
        )

        # Bedrock Agent를 사용하여 오류 메시지 분석
        analysis_prompt = (
            f"다음 오류 메시지를 분석해주세요:\n\n{original_error}\n\n"
            "다음 정보를 포함하여 분석 결과를 제공해주시고 최대한 Confluence와 S3에 동기화 된 Knowledge Base를 활용해 주세요.:\n"
            "1. 메시지 종류 (예: 오류, 경고, 정보)\n"
            "2. 메시지 발생 원인\n"
            "3. 가능한 해결 방법\n"
            "분석 결과는 한국어로 작성해주세요."
        )
        
        analysis_result = invoke_bedrock_agent(
            input_text=analysis_prompt,
            analysis_type="analysis",
            session_id=thread_ts
        )

        # Expert에게 보낼 메시지 구성
        expert_notification = (
            f":rotating_light: *새로운 이슈가 할당되었습니다*\n\n"
            f"*할당자*: <@{requesting_user}>\n"
            f"*원본 에러 메시지*:\n```{original_error}```\n"
            f"*Bedrock Agent 분석 결과*:\n```{analysis_result}```\n"
            f"*추가 메시지*:\n{message_content}\n\n"
            f"*원본 스레드*: {create_thread_link(channel_id, thread_ts)}"
        )

        # Expert에게 DM 보내기
        send_slack_message(
            channel=f"@{expert_user}",
            text=expert_notification
        )

        # 원본 스레드에 할당 완료 메시지 보내기
        thread_notification = (
            f":white_check_mark: *Expert 할당이 완료되었습니다*\n"
            f"• 할당된 Expert: <@{expert_user}>\n"
            f"• 할당자: <@{requesting_user}>\n"
            f"• 할당 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"• 전달된 메시지: {message_content}\n"
            f"• Bedrock Agent 분석이 완료되어 Expert에게 전달되었습니다."
        )
        
        send_slack_message(
            channel_id,
            text=thread_notification,
            thread_ts=thread_ts
        )

    except Exception as e:
        logger.error(f"Error in expert assignment: {str(e)}")
        return {
            "response_action": "errors",
            "errors": {
                "message_content": f"Error processing request: {str(e)}"
            }
        }

    return {"response_action": "clear"}

def create_thread_link(channel_id, thread_ts):
    """Slack 스레드 링크 생성"""
    workspace_url = "https://awschatopswor-g0x9719.slack.com"  # 워크스페이스 URL로 변경 필요
    return f"{workspace_url}/archives/{channel_id}/p{thread_ts.replace('.', '')}"

def open_expert_modal(trigger_id, channel_id, thread_ts):
    """Expert 할당 모달 오픈"""
    modal_view = {
        "type": "modal",
        "callback_id": "expert_assignment",
        "private_metadata": json.dumps({"channel": channel_id, "thread_ts": thread_ts}),
        "title": {"type": "plain_text", "text": "Expert 할당"},
        "submit": {"type": "plain_text", "text": "할당"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*이슈를 할당할 Expert를 선택하고 메시지를 입력해주세요.*"
                }
            },
            {
                "type": "input",
                "block_id": "expert_user",
                "element": {
                    "type": "users_select",
                    "action_id": "user_select",
                    "placeholder": {"type": "plain_text", "text": "Expert 선택"}
                },
                "label": {"type": "plain_text", "text": "할당할 Expert"}
            },
            {
                "type": "input",
                "block_id": "message_content",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "message_input",
                    "multiline": True,
                    "placeholder": {"type": "plain_text", "text": "Expert에게 전달할 메시지를 입력하세요"}
                },
                "label": {"type": "plain_text", "text": "메시지 내용"}
            }
        ]
    }

    try:
        WebClient(token=OAUTH_TOKEN).views_open(
            trigger_id=trigger_id,
            view=modal_view
        )
    except SlackApiError as e:
        logger.error(f"Error opening modal: {e.response['error']}")
        send_slack_message(channel_id, f"모달 열기 실패: {e.response['error']}", thread_ts)
    
def lambda_handler(event, context):

    print(event)
    
    # 모달 제출 이벤트 처리
    if event.get('type') == 'view_submission':
        if event['view']['callback_id'] == 'ticket_creation':
            handle_view_submission(event)
            return {'statusCode': 200}
        elif event['view']['callback_id'] == 'expert_assignment':
            handle_expert_assignment(event)
            return {'statusCode': 200}
    
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
        send_slack_message(channel_id, f"저는 Error MSG를 전달하는 Bot 입니다. ", thread_ts)
        send_slack_message(channel_id, f"<@q> ask bora "+"에게 이 오류에 대한 분석을 요청할게\n" + f"*MSG 원문*:\n{error_message}", thread_ts)
        send_slack_message(channel_id, "분석중이니 잠시만 기다려주세요.", thread_ts)        
    elif bt_value == "click_reporting":
        send_slack_message(channel_id, "Reporting 생성 중입니다. 잠시만 기다려주세요.", thread_ts)
        get_comments_thread(channel_id, thread_ts)
    elif bt_value == "click_awscase":
        # AWS Case Open 모달 창 오픈
        trigger_id = event["trigger_id"]
        open_ticket_modal(trigger_id, channel_id, thread_ts)
    elif bt_value == "click_expert":
        # Expert 할당 모달 창 오픈
        trigger_id = event["trigger_id"]
        open_expert_modal(trigger_id, channel_id, thread_ts)

    return {"statusCode": 200}
