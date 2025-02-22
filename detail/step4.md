## Step 4: AWS Lambda와 Amazon API Gateway로 Slack과 Confluence 연동

### 목표
AWS Lambda와 API Gateway를 활용해 Slack 명령어로 Confluence에 데이터를 기록하는 기능 구현.

### 실습 내용
1. Amazon API Gateway에서 HTTP 엔드포인트 생성.
2. AWS Lambda 함수 작성:
   - Slack 명령어 처리 및 Confluence API 호출 로직 구현.
3. API Gateway와 Lambda 연결.
4. Slack 명령어 테스트:
   - 특정 메시지를 입력하여 Confluence에 데이터 기록 여부 확인.

---