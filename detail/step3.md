## Step 3: Log 모니터링 및 알림 메시지 수신을 위한 Slack 구성 및 AWS와 연동

### 목표
Slack 채널을 구성하고 AWS 서비스와 연동하여 로그 모니터링 및 알림 메시지를 수신합니다.

<img width="914" alt="image" src="https://github.com/user-attachments/assets/66dd8fe6-4fae-4f8b-9679-777f54a3b426" />



### 실습 내용
1. Slack에서 새로운 앱 생성 및 Webhook URL 설정.
2. AWS Lambda 함수 생성:
   - 특정 이벤트 발생 시 Slack으로 알림 전송.
3. CloudWatch와 Lambda 연동:
   - 로그 이벤트 발생 시 Lambda 트리거 설정.
4. Slack 채널에서 알림 메시지 수신 테스트.

---
