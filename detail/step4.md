## Step 4: AWS Lambda와 Amazon API Gateway로 Slack과 Confluence 연동

### 목표
AWS Lambda와 API Gateway를 활용해 Slack 명령어로 Confluence에 데이터를 기록하는 기능 구현.<br>
<img width="1007" alt="image" src="https://github.com/user-attachments/assets/53bb8b61-3285-4f10-adf5-f8c1e70a079c" />

***
### 실습 내용
1. AWS Lambda가 발생시키는 Test Error MSG를 Slack이 수신 할 수 있도록 Slack Custom APP을 생성.
2. AWS Secret Manager를 생성하고, Slack Custom APP, Atlassian Confluence 의 Secure Key등을 Secret value로 저장.
3. AWS Lambda 함수 2개 수정:
   - chatops-stack-msg-to-slack-function: Error MSG를 Slack으로 전달하는 역할
   - chatops-stack-gw-to-slack-function: Agent 를 통해 Bedrock LLM 호출 및 Confluence에 Thread 내용요약 후 리포팅하는 역할
4. Amazon API Gateway와 AWS Lambda통합 연결.
5. Slack에서 최종 테스트:
   - Error MSG를 Bedrock 의 LLM을 통해 분석 확인.
   - Thread내 누적된 내용이 요약되어 Confluence에 리포팅 되는지 확인.
  
---
## 1. AWS Lambda가 발생시키는 Test Error MSG를 Slack이 수신 할 수 있도록 Slack Custom APP을 생성.<br>
최초 AWS Lambda로 부터 Slack Channel 로 수신되는 원본 Error Message 에 대해 3가지 Action[Watching | To Bedrock Agent | Reporting] 을 담당자가 할 수 있게 도와주는 역할을 제공하는 Slack App 을 하나 생성합니다. 이 App은 Slack에서 각 버튼을 선택하면 사용자의 요청을 수행해 주며, 즉시 결과를 Thread 에 알립니다.

Step3에서 Slack에 가입했던 Web브라우저(이유:Login 세션유지)에서 [Slack API 페이지](https://api.slack.com/apps)에 접속합니다. 
여기서 **Create an App** > From a manifest 로 APP을 생성해줍니다. 
<img width="1294" alt="image" src="https://github.com/user-attachments/assets/358a8bbf-f170-44c7-9782-a6dc3e7b25ae" />

- Pick a workspace to develop your app in:는 여러분의 워크스페이스를 선택! 후 Next로 완료합니다.
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/ba82ee12-1fa2-4b6d-a305-3ed82c79be86" />

<img width="1283" alt="image" src="https://github.com/user-attachments/assets/abfc141d-d208-4009-bfb7-2f4d718cd0ca" />

- Basic Information 페이지에서 아래로 스크롤 하여 아래 Field의 Values 를 채워넣고 Display Information 설정을 완료합니다. **Save** 해줍니다.<br>

| Field                   | Name                                                                                                                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| App name        | ```msg-fwd```                                                                                                                                                                                                               |
| Short description     | ```This is a bot that delivers AWS Alert messages.```                                                                                                                                                                                                           |
| Long description  | ```This bot performs the function of delivering notification messages from Slack to the AWS Bedrock Agent connector. Through this bot, it seems possible to monitor the status of the AWS environment in real-time and respond quickly.```                                                                                                                                                                                                                        |

<img width="1311" alt="image" src="https://github.com/user-attachments/assets/4582a89b-8a63-4300-9920-52bcebf0d2c9" /><br>

- Basic Information > OAuth & Permissions > Scopes > Bot Token Scopes 추가하기 
<img width="1278" alt="image" src="https://github.com/user-attachments/assets/1e7de8ff-c811-4678-a11b-ef131fcaa4d7" />

<img width="718" alt="image" src="https://github.com/user-attachments/assets/525fa48d-bfa3-4376-9ae1-ffab30edaaf8" />

- Slack에서 APP과 User간의 원활한 대화를 위해서 Permission scopes 을 잘 설정해 줘야 합니다.<br>
이 Workshop 에서 필요한 옵션들은 아래와 같이 참고하여 추가해 주세요.<br>
```assistant:write``` , ```channels:history``` , ```channels:read``` , ```channels:write.topic``` , ```chat:write``` , ```chat:write.public``` , ```groups:history``` , ```groups:write``` , ```im:history``` , ```incoming-webhook``` , ```mpim:history```<br>

<img width="701" alt="image" src="https://github.com/user-attachments/assets/248e0327-365b-4ac3-a55f-c03d2d90fb04" />

- Basic Information > OAuth Tokens > Bot User OAuth Token 생성하기(OAuth Token을 발급하기 위함)
<img width="1275" alt="image" src="https://github.com/user-attachments/assets/0c8dcaad-2672-4471-a961-f9ab16737d77" />

- 이 App을 aws-chatops-workshop 채널에 배포하기
<img width="1249" alt="image" src="https://github.com/user-attachments/assets/de8f15ce-9e2a-4b0f-893b-a54ef5f1d1d1" />

- Basic Information > OAuth Tokens > 발급된 Bot User OAuth Token 값을 따로 저장하세요.(**AWS Secret Manager** 에 보관예정)
<img width="1274" alt="image" src="https://github.com/user-attachments/assets/01769d24-304f-40db-be54-0674601af23a" />

- Slack내 aws-chatops-workshop 채널에 위에서 생성한 msg-fwd APP이 배포되어 있는 것을 확인합니다.
<img width="898" alt="image" src="https://github.com/user-attachments/assets/458e6880-58bf-4cd4-b776-f7e869bdb8cf" />

- Slack내 aws-chatops-workshop 채널에 msg-fwd APP을 초대(@msg-fwd)해 줍니다.
<img width="910" alt="image" src="https://github.com/user-attachments/assets/a72a23e4-a69b-4ab1-8389-9b92b0b8ac1d" />

## 2. AWS Secret Manager를 생성하고, Slack Custom APP, Atlassian Confluence 의 Secure Key등을 Secret value로 저장.
- 이 Secret value 들은 AWS Lambda가 API를 통해서 Slack, Atlassian Confluence 간 통신하는데 환경변수로 사용됩니다.<br>

[AWS Secrets Manager](https://us-west-2.console.aws.amazon.com/secretsmanager/listsecrets?region=us-west-2)에 접속합니다.<br>
새로운 Secret을 생성하고, 아래와 같이 Key/value pairs를 넣어 줍니다.<br>
다음과 같이 6가지의 Key/Value를 저장합니다.<br>
<img width="1450" alt="image" src="https://github.com/user-attachments/assets/3b9fc537-a0f1-4d1c-9e95-fa47e208d80e" /><br>

| Secret key                   | Secret value                                                                                                                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| slack_token        | ```여러분 Slack Custom APP의 Bot User OAuth Token```                                                                                                                                                                                                               |
| wiki_api_key     | ```강사 제공```                                                                                                                                                                                                           |
| wiki_url  | ```https://aws-chatops-workshop.atlassian.net/wiki```                                                                                                                                                                                                                        |
| wiki_user  | ```강사 제공```                                                                                                                                                                                                        |
| bedrock_agent        | ```여러분의 AgentID```                                                                                                                                                                                                          |
| bedrock_agent_alias        | ```여러분의 Agent AliasID```                                                                                                                                                                                          |

중요! Secret name은 정확히 ```wn/chatops/secret``` 로 입력 후 저장해 주세요.<br>
(AWS Lambda에서 slack, confluence 인증을 위해 이 value name을 환경변수로 참고합니다.<br>
<img width="1464" alt="image" src="https://github.com/user-attachments/assets/631b66b6-034b-4ee6-8b1a-1f0edb0c8f7f" />

## 3. AWS Lambda 함수 2개 수정:
이 Workshop에서 가장 중요한 역할을 수행하는 AWS Lambda Function 2개는 이미 실습시작 시 여러분이 수행한 Cloudforamtion을 통해서 배포되어 있습니다.
먼저 강제로 Error MSG를 발생시키고 Slack으로 전달하는 역할을 수행하는 **chatops-stack-msg-to-slack-function** 을 수정해 보겠습니다.<br>
**1st - AWS Lambda Function:** [chatops-stack-msg-to-slack-function 바로가기](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/chatops-stack-msg-to-slack-function?tab=code)<br>

🚩44번 Line의 channel에 ```aws-chatops-workshop``` 로 변경 후 **Deploy** 합니다.<br>
![image](https://github.com/user-attachments/assets/642a7a66-55ec-4e56-a3f3-25d6f3888e1d)

Configuration > Environment variables > Edit <br>
![image](https://github.com/user-attachments/assets/dad985cd-7a87-4ef6-8dd5-31e673992b47)

Add environment variable 에 아래와 같이 Value를 입력 후 저장합니다.<br>
![image](https://github.com/user-attachments/assets/2cddd996-6d68-460f-a687-e9a8306be0f1)

**chatops-stack-msg-to-slack-function** 을 Test 해보겠습니다.<br>
👏👏👏우측에 Slack채널(aws-chatops-workshop)에 **chatops-stack-msg-to-slack-function** 로 부터 Erro MSG를 정상적으로 수집했습니다.<br>
![image](https://github.com/user-attachments/assets/c1a198cc-983a-4959-b83d-0b662cba9e47)


이번에는 Agent 를 통해 Bedrock LLM 호출 및 Confluence에 Thread 내용을 요약 후 리포팅하는 역할을 수행하는 **chatops-stack-gw-to-slack-function** 을 수정해 보겠습니다.<br>
**2nd - AWS Lambda Function:** [chatops-stack-gw-to-slack-function 바로가기](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/chatops-stack-gw-to-slack-function?tab=code)<br>

🚩140번 Line의 send_slack_message에 "<@aws> ask bora"를 ```<@q> ask 커넥터이름``` 로 변경 후 **Deploy** 합니다.<br>
(2025년 2월 AWS Chatbot이 Amazon Q Developer로 이름이 변경되며, 커넥터 호출방식도 변경됨)
![image](https://github.com/user-attachments/assets/e985fa6e-9775-424f-bf22-1e3d74603487)


Configuration > Environment variables > Edit <br>
![image](https://github.com/user-attachments/assets/dad985cd-7a87-4ef6-8dd5-31e673992b47)

Add environment variable 에 아래와 같이 Value를 입력 후 저장합니다.<br>
![image](https://github.com/user-attachments/assets/2cddd996-6d68-460f-a687-e9a8306be0f1)

Triggers 메뉴를 보면, Amazon API Gateway와 통합되어 있는 2개를 확인할 수 있습니다.<br>
그중 아래의 2번째 URL을 복사해서 따로 저장해 둡니다.<br>
![image](https://github.com/user-attachments/assets/071a2552-7ba2-461f-91d7-5b5538e7619e)

Slack에 가입했던 Web브라우저(이유:Login 세션유지)에서 [Slack API 페이지](https://api.slack.com/apps)에 접속합니다.<br> 
Basic Information 페이지의 Interactivity & Shortcuts 메뉴를 On으로 변경하면, Interactivity를 위한 Request URL을 입력하게 되어 있습니다.<br>
이곳에 바로 위에 AWS Lambda의 트리거로 설정된 Amazon API Gateway URL을 입력하고 꼭 **SAVE** 해줍니다.<br>
![image](https://github.com/user-attachments/assets/0b5d73a4-2113-487a-9ef3-98faeada4cf8)

👏👏👏 모든 작업이 완료 되었습니다.<br> 
정리해보면, Slack에서 MSG를 수신하고 최초 제공되는 버튼을 선택 시 Amazon API Gateway와 통합된 AWS Lambda Function(chatops-stack-gw-to-slack-function)을 호출하게 됩니다.<br>
이후 Function은 정의된 버튼에 대한 각각의 Action을 수행하게 되는데 이제 Slack에서 다른 2가지 버튼을 동작해 보겠습니다.<br>

- **To bedrock agent** 버튼 선택시 Agent를 호출하여 Bedrock의 LLM에게 분석을 요청합니다.<br>
  1. 먼저 팀 자산이 임베딩 된 Amazon Bedrock Knowledge Bases를 검색하고 수신했던 MSG와 유사한 결과를 찾습니다.
  2. 이후 이 결과를 바탕으로 LLM은 원인, 분석, 해결, 요약 등 Step2 Agent를 생성할 때 Prompt로 설정한 의도에 최대한 맞춰서 답을 줍니다.
![image](https://github.com/user-attachments/assets/9448b528-4efc-473a-a0eb-b4f95a61bcaa)

- Connector를 추가 호출하면서 좀 더 구체적인 질문도 해봅니다.
![image](https://github.com/user-attachments/assets/73c86b0d-fa0b-4c66-8f92-4043b32602aa)

- **Reporting** 버튼 선택시 Slack의 현재 Thread에 나누던 모든 내용을 요약하여 Atlassian Confluence에 게시합니다.
![image](https://github.com/user-attachments/assets/1456751a-5819-4868-956c-5c2d7e7ec7ed)


여기까지 해서 이 Workshop의 모든 실습이 완료 되었습니다.<br>
## 감사합니다.







