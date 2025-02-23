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






