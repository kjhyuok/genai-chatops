## Step 2: Amazon Bedrock Agent 생성 및 Knowledge Bases와 연동

### 목표
Amazon Bedrock Agent를 생성하고, 이전 단계에서 구성한 Knowledge Bases와 연동하여 에이전트가 데이터를 활용하도록 설정합니다.

### 실습 내용
1. Amazon Bedrock 메뉴에서 Agent 생성.
2. 에이전트의 역할과 사용 모델(FM) 정의.
3. 에이전트를 Knowledge Bases와 연결.
4. 에이전트 테스트:
   - 특정 질문을 입력하여 Knowledge Base 데이터를 기반으로 한 응답 확인.

---
## 1. Amazon Bedrock 메뉴에서 Agent 생성하기.<br>
메뉴이동: [Amazon Bedrock Agents](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/agents)<br>

**1. Amazon Bedrock 좌측 페이지 메뉴에서 Agent를 선택합니다. Create<br>**
- Create agent를 눌러서 Name을 ```agent-quick-start-2025``` 로 지정합니다.<br>
![image](https://github.com/user-attachments/assets/5217c112-4ae4-4475-a25f-e0344daaa019)

- Agent가 사용할 FM(Foundation Model)은 Anthropic사의 Claude 3.5 Sonnet v1으로 선택하고 Apply 해줍니다.<br>
![image](https://github.com/user-attachments/assets/3f6f05cb-00e5-4d98-a5d7-ce82fd90477c)

- Instructions for the Agent에는 아래와 같이 Agent가 수행할 작업에 대해 명확하고 구체적인 지침을 위한 Prompt를 입력해 줍니다.<br>
![image](https://github.com/user-attachments/assets/596bc42f-4a04-4dbc-b44b-35e044742a2e)<br>
```You are an agent helping IT service operations teams in large companies that operate the AWS cloud with technical issues. You will receive the following questions from IT operations teams on slack. The questions are very technical, and they are error messages or critical alarms generated not only from AWS, but also from various types of solutions such as 3rd party security and databases. 1.When the operations team asks you to analyze any message, you first check Confluence and S3 connected to Amazon Bedrock's KnowledgeBase. 2.Based on that information, you should use Amazon Bedrock's Claude3 LLM, summarize, and give an accurate answer in the form below. 2-1. For incoming messages, please provide analyzed content such as issue details, causes, solutions, etc. 2-2. @aws From the user's question called ask alias, check Confluence and S3 connected to Amazon Bedrock's KnowledgeBase to find answers based on past content as much as possible. In summary, you're an agent for seamless communication between Slack and Amazon Bedrock. If you describe the information you've found, leave that URL (Confluence or S3 bucket) Of course, all questions must be answered in Korean.```

- 바로 아래에 Additional settings에서는 Enabled 선택합니다.<br>
(Agent가 사용자와 Interaction중에 충분한 정보가 없는 경우 Agent가 사용자에게 추가 정보를 요청할 수 있도록 지원 합니다.)
![image](https://github.com/user-attachments/assets/5e2661bb-c5e3-45a1-bff2-6ddae6ebc9fc)

- 우측 Test창에서 Agent가 정상적으로 설정되었는지 Prepare 를 선택<br>
![image](https://github.com/user-attachments/assets/de9c469c-c5a0-492d-8be4-575a570a031b)

- Prepare가 완료되면 Agent의 Status가 초록색 **PREPARED** 인지 확인 합니다.<br>
![image](https://github.com/user-attachments/assets/08a11f58-6ab6-4d88-8436-7ecd4c561d48)

- Agent resource role이 Create and use a new service role로 선택되었는지 확인하고 지금까지 내용을 **Save and Exit**을 통해서 저장해 줍니다.(Agent 메뉴 우측상단)<br>
![image](https://github.com/user-attachments/assets/167f3e8a-98da-4d22-b33c-62f183db8629)

## 2. Agent를 Knowledge Bases를 연동하기.<br>
- 이제는 add 선택하여 앞서 생성한 Agent에 Step1에서 생성했던 Knowledge Bases를 연동해 봅니다.<br>
![image](https://github.com/user-attachments/assets/58fa9c75-ab0e-4e38-a1bd-6d6094d05575)

- Agent가 답변에 참조 할 수 있도록 Step1에서 생성했던 Knowledge Bases(agent-quick-start-2025)를 선택하고,<br> 
![image](https://github.com/user-attachments/assets/010d500f-28a5-4648-8873-25c67a935a58)

- 아래와 같이 Knowledge Base instruction for agent를 작성해주고 Add 해줍니다.<br>
이렇게 Instruction을 작성하게 되면 Knowledge Bases가 Agent와 상호 작용하는 방식에 영향을 미치게 됩니다.<br>
```Refer to S3 & Confluence docs in Bedrock for AWS cloud questions from IT ops team via Slack. Use Claude Sonnet 3.5 v1 on Amazon Bedrock to accurately summarize and answer questions.```
![image](https://github.com/user-attachments/assets/413f3c6e-e726-4aaa-815a-e352f81c0701)

- Agent메뉴로 복귀해서 이 Agent의 Alias 만들어 보겠습니다.<br>
Create alias > Alias name > ```aws-chatops-workshop``` 입력합니다.
![image](https://github.com/user-attachments/assets/fdcc6e2f-5c93-4f6a-bf81-c4b81805d90a)

- 아래와 같이 Versioning되며, Alias ID: 5OEZZ8BA7K | Alias name: aws-chatops-workshop 이 생성되었습니다. 
![image](https://github.com/user-attachments/assets/fae22c79-10ae-4b6b-aef7-a655e452dc65)

***

여기까지 Amazon Bedrock Agent 생성하고 Step1에서 생성한 Amazon Knowledge Bases와 연동을 완료 하셨습니다.

### 이제,  Log 모니터링 및 알림 메시지 수신을 위한 Slack 구성 및 AWS와 연동하는 다음 단계 실습으로 이동합니다.<br>
[Step 3:Log 모니터링 및 알림 메시지 수신을 위한 Slack 구성 및 AWS와 연동](step3.md)














