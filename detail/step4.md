## Step 4: AWS Lambda와 Amazon API Gateway로 Slack과 Confluence 연동

### 목표
AWS Lambda와 API Gateway를 활용해 Slack 명령어로 Confluence에 데이터를 기록하는 기능 구현.<br>
<img width="1007" alt="image" src="https://github.com/user-attachments/assets/53bb8b61-3285-4f10-adf5-f8c1e70a079c" />


step4 는 가장 난이도높음!

시작시

1.slack 앱생성-설정-키값생성

2.new kms 에 키값넣기

3.lambda 2 개 수정, kms 환경변수추가

4.api gw 에 wiki url 연결후 lambda 통합

5.최종테스트!

- 메시지분석
- 요약
- 게시

### 실습 내용
1. Amazon API Gateway에서 HTTP 엔드포인트 생성.
2. AWS Lambda 함수 작성:
   - Slack 명령어 처리 및 Confluence API 호출 로직 구현.
3. API Gateway와 Lambda 연결.
4. Slack 명령어 테스트:
   - 특정 메시지를 입력하여 Confluence에 데이터 기록 여부 확인.
  
   - 
3. AWS Lambda 함수 생성:(CloudFormation으로 이미 Workshop에 배포완료)
   - 특정 이벤트 발생시 메시지를 Slack으로 알림 전송하는 역할 수행.
   - Message to Lambda   - 이 Workshop에서는 AWS Lambda를 통해서 Hard Coding 된 준비된 특정 Error 이벤트를 발생합니다.
5. Slack 채널에서 알림 메시지 수신 테스트 확인.
---
