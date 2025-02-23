## Step 4: AWS Lambda와 Amazon API Gateway로 Slack과 Confluence 연동

### 목표
AWS Lambda와 API Gateway를 활용해 Slack 명령어로 Confluence에 데이터를 기록하는 기능 구현.<br>
<img width="1007" alt="image" src="https://github.com/user-attachments/assets/53bb8b61-3285-4f10-adf5-f8c1e70a079c" />

***
### 실습 내용
1. AWS Lambda가 발생시키는 Test Error MSG를 Slack이 수신 할 수 있도록 Slack Custom APP을 생성.
2. AWS Secret Manager를 생성하고, Slack Custom APP, Atlassian Confluence 의 Secure Key등을 Secret value로 저장.
   - 이 Secret value 들은 AWS Lambda가 API를 통해서 Slack, Atlassian Confluence 간 통신하는데 환경변수로 사용됩니다.
   - 다음과 같이 6가지의 Key/Value를 저장합니다.<br>

| Secret key                   | Secret value                                                                                                                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| slack_token        | ```여러분 Slack Custom APP의 Token Key```                                                                                                                                                                                                               |
| wiki_api_key     | ```강사 제공```                                                                                                                                                                                                           |
| wiki_url  | ```https://aws-chatops-workshop.atlassian.net/wiki```                                                                                                                                                                                                                        |
| wiki_user  | ```강사 제공```                                                                                                                                                                                                        |
| bedrock_agent        | ```여러분의 AgentID```                                                                                                                                                                                                          |
| bedrock_agent_alias        | ```여러분의 Agent AliasID```                                                                                                                                                                                          |

3. AWS Lambda 함수 2개 수정:
   - chatops-stack-msg-to-slack-function: Error MSG를 Slack으로 전달하는 역할
   - chatops-stack-gw-to-slack-function: Agent 를 통해 Bedrock LLM 호출 및 Confluence에 Thread 내용요약 후 리포팅하는 역할
4. Amazon API Gateway와 AWS Lambda통합 연결.
5. Slack에서 최종 테스트:
   - Error MSG를 Bedrock 의 LLM을 통해 분석 확인.
   - Thread내 누적된 내용이 요약되어 Confluence에 리포팅 되는지 확인.
  
---



