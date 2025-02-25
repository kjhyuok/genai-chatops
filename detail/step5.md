## step 5: 시나리오 기반 테스트

### 목표
테스트 데이터를 기반으로 지금까지 구축한 솔루션을 활용해 봅니다.

### 시나리오
1. AWS Lambda(chatops-stack-msg-to-slack-function)에 다양한 우리회사의 주요 수신되는 Message들을 붙여서 Test로 Slack에 메시지 수신해보기
2. Bedrock Agent로 분석 요청하고 결과 확인(요청시마다 응답결과가 조금씩 다를 수 있음)
3. 커넥터를 통한 상세 분석(요청시마다 응답결과가 조금씩 다를 수 있음, Knowledge Bases 튜닝이 필요한 영역)
4. 실습자간에 초대하여 대화를 나누고, 해당 Thread내용을 Reporting 요청 해보기 등 
