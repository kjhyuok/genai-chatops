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

def send_slack_message(channel, text=None, thread_ts=None, blocks=None):
    """Slack 메시지 전송"""
    message = {
        "channel": channel,
        "thread_ts": thread_ts
    }
    
    if blocks:
        message["blocks"] = blocks
    elif text:
        message["text"] = text
    else:
        raise ValueError("Either text or blocks must be provided")
        
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=SLACK_HEADERS,
        json=message
    )
    
    if not response.json().get("ok"):
        logger.error(f"Failed to send message: {response.json().get('error')}")
        raise Exception(f"Failed to send message: {response.json().get('error')}")
    
    return response.json()

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

        # Bedrock Agent를 사용하여 Expert에게 보낼 메시지 생성
        expert_message_prompt = (
            f"다음 정보를 바탕으로 Expert에게 보내는 공손한 메시지를 작성해주세요:\n\n"
            f"1. 원본 에러 메시지:\n{original_error}\n\n"
            f"2. 추가 메시지:\n{message_content}\n\n"
            f"3. Bedrock Agent 분석 결과:\n{analysis_result}\n\n"
            "다음 형식으로 작성해주세요:\n"
            "1. 인사말과 상황 설명\n"
            "2. 문제의 중요성과 긴급성\n"
            "3. Expert의 도움이 필요한 이유\n"
            "4. 감사 인사\n"
            "모든 내용은 한국어로 작성하고, 공손하고 전문적인 어조를 사용해주세요."
        )
        
        expert_message = invoke_bedrock_agent(
            input_text=expert_message_prompt,
            analysis_type="analysis",
            session_id=thread_ts
        )

        # Expert에게 보낼 메시지 블록 구성
        expert_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":rotating_light: *새로운 이슈가 할당되었습니다*\n\n*할당자*: <@{requesting_user}>\n\n*전달 메시지*\n{expert_message}\n\n*원본 스레드*: {create_thread_link(channel_id, thread_ts)}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "거절하기",
                            "emoji": True
                        },
                        "style": "danger",
                        "value": f"{channel_id}_{thread_ts}",
                        "action_id": "reject_issue"
                    }
                ]
            }
        ]

        # Expert에게 DM 보내기
        send_slack_message(
            channel=f"@{expert_user}",
            blocks=expert_blocks
        )

        # 원본 스레드에 할당 완료 메시지 보내기
        thread_notification = (
            f":white_check_mark: *Expert 할당이 완료되었습니다*\n"
            f"• 할당된 Expert: <@{expert_user}>\n"
            f"• 할당자: <@{requesting_user}>\n"
            f"• 할당 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"• Bedrock Agent가 메시지를 분석하고 Expert에게 전달했습니다."
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

def open_reject_modal(trigger_id, channel_id, thread_ts):
    """이슈 거절 모달 오픈"""
    modal_view = {
        "type": "modal",
        "callback_id": "issue_rejection",
        "private_metadata": json.dumps({"channel": channel_id, "thread_ts": thread_ts}),
        "title": {"type": "plain_text", "text": "이슈 거절"},
        "submit": {"type": "plain_text", "text": "거절"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*이슈 거절 사유를 입력해주세요.*"
                }
            },
            {
                "type": "input",
                "block_id": "rejection_reason",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "reason_input",
                    "multiline": True,
                    "placeholder": {"type": "plain_text", "text": "거절 사유를 입력하세요"}
                },
                "label": {"type": "plain_text", "text": "거절 사유"}
            }
        ]
    }

    try:
        WebClient(token=OAUTH_TOKEN).views_open(
            trigger_id=trigger_id,
            view=modal_view
        )
    except SlackApiError as e:
        logger.error(f"Error opening reject modal: {e.response['error']}")
        send_slack_message(channel_id, f"모달 열기 실패: {e.response['error']}", thread_ts)

def handle_issue_rejection(payload):
    """이슈 거절 처리"""
    try:
        metadata = json.loads(payload["view"]["private_metadata"])
        values = payload["view"]["state"]["values"]
        
        channel_id = metadata["channel"]
        thread_ts = metadata["thread_ts"]
        rejecting_user = payload["user"]["id"]
        rejection_reason = values["rejection_reason"]["reason_input"]["value"]

        # Bedrock Agent를 사용하여 거절 메시지 생성
        rejection_prompt = (
            f"다음 거절 사유를 바탕으로 공손한 거절 메시지를 작성해주세요:\n\n"
            f"거절 사유: {rejection_reason}\n\n"
            "다음 형식으로 작성해주세요:\n"
            "1. 거절 의사 표명\n"
            "2. 거절 사유 설명\n"
            "3. 대안 제시 (가능한 경우)\n"
            "4. 감사 인사\n"
            "모든 내용은 한국어로 작성하고, 공손하고 전문적인 어조를 사용해주세요."
        )
        
        rejection_message = invoke_bedrock_agent(
            input_text=rejection_prompt,
            analysis_type="analysis",
            session_id=thread_ts
        )

        # 원본 스레드에 거절 메시지 보내기
        rejection_notification = (
            f":x: *이슈가 거절되었습니다*\n"
            f"• 거절한 Expert: <@{rejecting_user}>\n"
            f"• 거절 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"• 거절 사유:\n{rejection_message}"
        )
        
        send_slack_message(
            channel_id,
            text=rejection_notification,
            thread_ts=thread_ts
        )

    except Exception as e:
        logger.error(f"Error handling issue rejection: {str(e)}")
        return {
            "response_action": "errors",
            "errors": {
                "rejection_reason": f"Error processing rejection: {str(e)}"
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
    
def open_meeting_modal(trigger_id, channel_id, thread_ts):
    """미팅 일정 조율 모달 오픈"""
    # 날짜 선택 블록 생성
    date_blocks = []
    for i in range(3):
        date_blocks.extend([
            {
                "type": "input",
                "block_id": f"meeting_date_{i}",
                "element": {
                    "type": "datepicker",
                    "action_id": f"date_select_{i}",
                    "initial_date": datetime.now().strftime("%Y-%m-%d"),
                    "placeholder": {"type": "plain_text", "text": f"미팅 날짜 {i+1} 선택"}
                },
                "label": {"type": "plain_text", "text": f"미팅 날짜 {i+1}"},
                "optional": True
            },
            {
                "type": "input",
                "block_id": f"meeting_time_{i}",
                "element": {
                    "type": "checkboxes",
                    "action_id": f"time_select_{i}",
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "오전 (09:00 ~ 12:00)"},
                            "value": "morning"
                        },
                        {
                            "text": {"type": "plain_text", "text": "오후 (13:00 ~ 18:00)"},
                            "value": "afternoon"
                        }
                    ]
                },
                "label": {"type": "plain_text", "text": f"시간대 {i+1}"},
                "optional": True
            }
        ])

    modal_view = {
        "type": "modal",
        "callback_id": "meeting_schedule",
        "private_metadata": json.dumps({"channel": channel_id, "thread_ts": thread_ts}),
        "title": {"type": "plain_text", "text": "미팅 일정 조율"},
        "submit": {"type": "plain_text", "text": "일정 제안"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*미팅 일정을 조율해보세요. 최대 3개의 날짜와 각각의 오전/오후 시간대를 선택할 수 있습니다.*"
                }
            },
            {
                "type": "input",
                "block_id": "participants",
                "element": {
                    "type": "multi_users_select",
                    "action_id": "users_select",
                    "placeholder": {"type": "plain_text", "text": "참석자 선택"}
                },
                "label": {"type": "plain_text", "text": "참석자"}
            }
        ] + date_blocks
    }

    try:
        WebClient(token=OAUTH_TOKEN).views_open(
            trigger_id=trigger_id,
            view=modal_view
        )
    except SlackApiError as e:
        logger.error(f"Error opening meeting modal: {e.response['error']}")
        send_slack_message(channel_id, f"모달 열기 실패: {e.response['error']}", thread_ts)

def handle_meeting_schedule(payload):
    """미팅 일정 제안 처리"""
    try:
        metadata = json.loads(payload["view"]["private_metadata"])
        values = payload["view"]["state"]["values"]
        
        # 참석자 목록 가져오기
        participants = values["participants"]["users_select"]["selected_users"]
        
        channel_id = metadata["channel"]
        thread_ts = metadata["thread_ts"]
        requesting_user = payload["user"]["id"]

        # 현재 스레드의 모든 메시지 가져오기
        response = requests.get(
            f"https://slack.com/api/conversations.replies?channel={channel_id}&ts={thread_ts}",
            headers=SLACK_HEADERS
        )
        
        if not response.json().get("ok"):
            raise Exception("Failed to fetch thread messages")
        
        messages = response.json().get("messages", [])
        thread_content = "\n".join(
            f"{msg.get('user', 'Unknown')}: {msg.get('text', '')}"
            for msg in messages
            if msg.get("text")
        )

        # Bedrock Agent를 사용하여 미팅 목적 생성
        purpose_prompt = (
            f"다음 대화 내용을 분석하여 미팅 목적을 생성해주세요:\n\n"
            f"{thread_content}\n\n"
            "다음 형식으로 작성해주세요:\n"
            "1. 이슈 요약\n"
            "2. 논의가 필요한 주요 사항\n"
            "3. 예상되는 미팅 결과\n"
            "모든 내용은 한국어로 작성해주세요."
        )
        
        meeting_purpose = invoke_bedrock_agent(
            input_text=purpose_prompt,
            analysis_type="analysis",
            session_id=thread_ts
        )

        # 선택된 날짜와 시간대 추출
        meeting_schedules = []
        for i in range(3):
            date_block = values.get(f"meeting_date_{i}", {}).get(f"date_select_{i}", {})
            time_block = values.get(f"meeting_time_{i}", {}).get(f"time_select_{i}", {})
            
            if date_block.get("selected_date") and time_block.get("selected_options"):
                date = date_block["selected_date"]
                times = [option["value"] for option in time_block["selected_options"]]
                
                for time in times:
                    time_text = "오전 (09:00 ~ 12:00)" if time == "morning" else "오후 (13:00 ~ 18:00)"
                    meeting_schedules.append(f"{date} {time_text}")

        if not meeting_schedules:
            return {
                "response_action": "errors",
                "errors": {
                    "meeting_date_0": "최소 하나의 날짜와 시간대를 선택해주세요."
                }
            }

        # 참석자 멘션 생성
        participant_mentions = " ".join([f"<@{user}>" for user in participants])

        # Bedrock Agent를 사용하여 초대 메시지 생성
        invitation_prompt = (
            f"다음 미팅 목적을 바탕으로 참석자들에게 전달할 공손한 초대 메시지를 작성해주세요:\n\n"
            f"미팅 목적:\n{meeting_purpose}\n\n"
            "다음 정보를 포함하여 작성해주세요:\n"
            "1. 미팅의 중요성\n"
            "2. 참석이 필요한 이유\n"
            "3. 공손한 초대 메시지\n"
            "메시지는 한국어로 작성해주세요."
        )
        
        invitation_message = invoke_bedrock_agent(
            input_text=invitation_prompt,
            analysis_type="analysis",
            session_id=thread_ts
        )
        
        # 미팅 일정 메시지 구성
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📅 미팅 일정 제안",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*제안자*\n<@{requesting_user}>"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*참석자*\n{participant_mentions}"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*제안 일정*"
                }
            }
        ]
        
        # 메시지 전송
        message = {
            "channel": channel_id,
            "thread_ts": thread_ts,
            "blocks": blocks
        }
        response = requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json=message)
        
        # 각 일정을 별도의 메시지로 전송하고 이모지 추가
        if response.json().get("ok"):
            for schedule in meeting_schedules:
                schedule_message = {
                    "channel": channel_id,
                    "thread_ts": thread_ts,
                    "text": f"• {schedule}"
                }
                schedule_response = requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json=schedule_message)
                
                if schedule_response.json().get("ok"):
                    schedule_ts = schedule_response.json().get("ts")
                    requests.post(
                        "https://slack.com/api/reactions.add",
                        headers=SLACK_HEADERS,
                        json={
                            "channel": channel_id,
                            "timestamp": schedule_ts,
                            "name": "white_circle"
                        }
                    )
        
        # 미팅 목적과 초대 메시지 전송
        purpose_blocks = [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*미팅 목적*\n{meeting_purpose}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*초대 메시지*\n{invitation_message}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "각 일정에 ✅ 이모지로 참석 여부를 선택해주세요. (✅ 를 확인하여 Invite 드리겠습니다.)"
                    }
                ]
            }
        ]
        
        purpose_message = {
            "channel": channel_id,
            "thread_ts": thread_ts,
            "blocks": purpose_blocks
        }
        requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json=purpose_message)
        
        return {"response_action": "clear"}
        
    except Exception as e:
        logger.error(f"Error handling meeting schedule: {str(e)}")
        return {
            "response_action": "errors",
            "errors": {
                "meeting_purpose": f"일정 제안 중 오류가 발생했습니다: {str(e)}"
            }
        }

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
        elif event['view']['callback_id'] == 'meeting_schedule':
            handle_meeting_schedule(event)
            return {'statusCode': 200}
        elif event['view']['callback_id'] == 'issue_rejection':
            handle_issue_rejection(event)
            return {'statusCode': 200}
    
    # 버튼 클릭 이벤트 처리
    if event.get('type') == 'block_actions':
        action_id = event['actions'][0]['action_id']
        if action_id == 'reject_issue':
            channel_thread = event['actions'][0]['value'].split('_')
            channel_id = channel_thread[0]
            thread_ts = channel_thread[1]
            trigger_id = event['trigger_id']
            open_reject_modal(trigger_id, channel_id, thread_ts)
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
    elif bt_value == "click_meeting":
        # 미팅 일정 조율 모달 창 오픈
        trigger_id = event["trigger_id"]
        open_meeting_modal(trigger_id, channel_id, thread_ts)
    elif bt_value == "click_expert":
        # Expert 할당 모달 창 오픈
        trigger_id = event["trigger_id"]
        open_expert_modal(trigger_id, channel_id, thread_ts)

    return {"statusCode": 200}
