## Step 3: Log 모니터링 및 알림 메시지 수신을 위한 Slack 구성 및 AWS와 연동

### 목표
Slack 채널을 구성하고 AWS 서비스와 연동하여 로그 모니터링 및 알림 메시지를 수신합니다.

<img width="914" alt="image" src="https://github.com/user-attachments/assets/5fadbc97-a93c-475b-9205-8f7b184f5190" />


### 실습 내용
1. Slack을 생성하고 Amazon Q Developer in chat applications(구: AWS Chatbot)를 배포.
2. AWS Lambda 함수 생성:(CloudFormation으로 이미 Workshop에 배포완료)
   - 특정 이벤트 발생시 메시지를 Slack으로 알림 전송하는 역할 수행.
   - Message to Lambda
3. CloudWatch와 Lambda 연동:
   - 이 Workshop에서는 AWS Lambda를 통해서 Hard Coding 된 준비된 특정 Error 이벤트를 발생합니다.
4. Slack 채널에서 알림 메시지 수신 테스트 확인.

---
## 1. Slack의 워크스페이스를 생성하고 Amazon Q Developer in chat applications(구: AWS Chatbot)를 배포.<br>
본 Workshop에서 활용할 Slack을 무료버전으로 간단히 만들어 봅니다. (🚩업무에 불편을 주지 않을 Pure한 실습용 E-Mail로 만들어 주세요.)<br>
[Slack 가입하기](https://slack.com/intl/ko-kr/get-started?utm_source=google&utm_medium=paid_search&utm_campaign=kr__20241202&gclid=EAIaIQobChMI94iphN_YiwMVIeoWBR2xUx5bEAAYASAAEgLbJvD_BwE&campaign=701ed00000BwjL3AAJ&lpt=1#/createnew)

<img width="682" alt="image" src="https://github.com/user-attachments/assets/b5dd436d-15bb-4f0b-a370-7828d39f2641" />

워크스페이스를 생성합니다. 
<img width="898" alt="image" src="https://github.com/user-attachments/assets/f9ca58e6-4984-431b-88d7-af2f3897f250" />
고유한 이름이어야 하므로 ```aws-chatops-workshop-본인Alias지정``` 후 본인의 Alias 를 적당히 저장 합니다.
<img width="1045" alt="image" src="https://github.com/user-attachments/assets/2b3fab17-b2f7-4ee7-933b-9086c578fc4c" />

무료플랜으로 생성 마무리 합니다.
<img width="1227" alt="image" src="https://github.com/user-attachments/assets/f9f4fe2d-1c6d-4148-85e8-411028a44785" />


Slack과 Amazon Bedrock Agent와의 Connector 역할을 수행할 Amazon Q Developer in chat applications 를 생성해 봅니다.
메뉴이동: [Amazon Q Developer in chat applications](https://us-east-2.console.aws.amazon.com/chatbot/home?region=us-west-2#/)

우측에서 채팅 클라이언트를 Slack으로 선택해주시고 클라이언트 구성선택을 해주세요.

<img width="1474" alt="image" src="https://github.com/user-attachments/assets/a2422105-7728-4680-bbb6-92d64a49a7be" />

다음과 같이 AWS Amazon Q Developer에서 Slack 워크스페이스에 액세스하기 위해 권한을 요청합니다.
<img width="1578" alt="image" src="https://github.com/user-attachments/assets/517ba415-7eb5-4d6f-9d4a-7a0f6a61f9d1" />

우측 상단에 다른워크스페이스 추가 **+** 를 선택하시면, Slack 워크스페이스에 join할 수 있는 도메인을 입력하게 됩니다.
여기서는 강사가 이미 생성해 놓은 워크스페이스를 입력해 주세요.<br>
워크스페이스의 Slack URL을 다음과 같이 복사해서 입력 > ```aws-chatops-workshop```

가급적 여러분의 회사의 Slack과 불필요한 채널 혼용을 막기 위해 Web브라우저를 통해서 Slack에 접근해 주세요.<br>
이렇게 들어온 Slack에는 앞서 Amazon Q Developer in chat applications 을 통해서 생성했던 Amazon Q가 APP에 배포되어 있는 것을 확인 할 수 있습니다.<br>
<img width="1065" alt="image" src="https://github.com/user-attachments/assets/526c1022-ed2e-4c3a-8269-1efcb94712a7" />



