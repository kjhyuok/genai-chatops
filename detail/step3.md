## Step 3: Log 모니터링 및 알림 메시지 수신을 위한 Slack 구성 및 AWS와 연동

### 목표
Slack 채널을 구성하고 AWS 서비스와 연동하여 로그 모니터링 및 알림 메시지를 수신합니다.

<img width="914" alt="image" src="https://github.com/user-attachments/assets/fd21b429-873a-4625-9903-6f698aac1bf2" />

### 실습 내용
1. Slack을 생성하고 AWS Chatbot(Q Developer)를 배포.
2. AWS Lambda 함수 생성:(CloudFormation으로 이미 Workshop에 배포완료)
   - 특정 이벤트 발생시 메시지를 Slack으로 알림 전송하는 역할 수행.
   - Message to Lambda
3. CloudWatch와 Lambda 연동:
   - 이 Workshop에서는 AWS Lambda를 통해서 Hard Coding 된 준비된 특정 Error 이벤트를 발생합니다.
4. Slack 채널에서 알림 메시지 수신 테스트 확인.

---
