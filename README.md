# 🤖AWS GenAI를 활용한 IT 서비스 운영 자동화

현대의 IT 인프라 환경은 그 규모와 복잡성이 기하급수적으로 증가하고 있습니다. 클라우드 네이티브 아키텍처의 도입이나 마이크로서비스 기반 애플리케이션의 확산으로 기업의 IT 운영팀이 대응해야 할 영역은 지속적으로 확장되고 있습니다. 특히 시스템 전반에서 발생하는 다양한 종류의 로그 데이터, 메트릭 그리고 메시지들을 효과적으로 분석하고 신속하게 대응하는 것이 중요한 과제로 떠오르고 있습니다. 
1. 신속한 장애 대응의 필요성
특히 운영중인 시스템에 장애가 발생할 경우, IT운영팀은 해당 원인을 신속히 파악하고 해결해야 하는데, 시스템 규모 그리고 아키텍처 복잡성으로 인해 증가된 정보는 에러 메시지 발생시 빠르게 근본 원인을 식별하기가 어렵습니다. 게다가 다양한 연관 솔루션을 운영한다면 IT운영팀의 부담은 더욱 가중됩니다.
2. 지식의 자산화 필요성
또한 장애가 해결된 이후에도 동일한 문제 발생 시 과거의 경험을 바탕으로 보다 빠르고 효율적으로 해결할 수 있다면 IT운영팀의 축적된 장애 대응 경험과 해결 노하우가 매우 중요한 자산입니다. 그래서 우리는 이러한 정보를 잘 요약된 내용으로 정리하여 추후 장애 시 활용한다면 장애의 빈도가 높은 모듈에 대한 개선 그리고 업무의 효율성을 높일 수 있습니다.

---

## 📋 목차
1. [프로젝트 소개](#프로젝트-소개)
2. [아키텍처 개요](#아키텍처-개요)
3. [필수 조건](#필수-조건)
4. [설치 및 설정](#설치-및-설정)
5. [사용 방법](#사용-방법)

---

## 프로젝트 소개

이 프로젝트는 ChatOps를 통해 운영 활동을 중앙화하고, AWS 리소스와 상호작용하며 알림 및 명령 실행을 지원합니다. 주요 기능은 다음과 같습니다:
- AWS 이벤트에 대한 실시간 알림 전송
- Slack 또는 Microsoft Teams에서 명령 실행
- DevOps 및 운영 워크플로우 간소화
  
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/b62f1c30-dad1-4943-9d15-15eeb223ca2a" />


---

## 아키텍처 개요

아래는 이 프로젝트의 기본 아키텍처입니다:

<img width="1474" alt="image" src="https://github.com/user-attachments/assets/3115ef37-a187-4d18-9f18-7c6b7b8e709f" />



1. **AWS Lambda**: Slack 또는 Teams의 요청을 처리.
2. **Amazon API Gateway**: Lambda 함수와 통신하는 HTTP 엔드포인트 제공.
3. **AWS Chatbot**: 알림 및 명령 처리를 위한 Slack/Teams 통합.
4. **Amazon Q(구 AWS Chatbot)**: 알림 메시지 전송.
5. **Amazon CloudWatch**: 모니터링 및 경고 생성.

---

## 필수 조건

이 프로젝트를 실행하려면 다음이 필요합니다:
- AWS 계정
- Slack 또는 Microsoft Teams 워크스페이스
- AWS CLI 설치 및 구성
- Node.js 또는 Python (Lambda 함수 개발용)

---

## 설치 및 설정

### 1️⃣ 코드 클론
git clone h........
cd aws-........

### 2️⃣ AWS 리소스 배포
AWS CLI 또는 CloudFormation 템플릿을 사용하여 리소스를 배포합니다.
aws cloudformation deploy --template-file template.yml --stack-name chatops-........

### 3️⃣ Slack/Teams 통합 설정
1. AWS Management Console에서 **AWS Chatbot** 서비스 열기.
2. Slack 또는 Microsoft Teams 채널 추가.
3. 필요한 권한 부여 및 채널 URL 설정.

### 4️⃣ 환경 변수 구성
`.env` 파일에 필요한 환경 변수를 추가합니다:
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
AWS_REGION=us-east-1

---



---

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
