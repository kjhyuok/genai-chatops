# AWS 기반 ChatOps 프로젝트

AWS를 활용하여 ChatOps 환경을 구축하고 관리하기 위한 프로젝트입니다. 이 프로젝트는 AWS Lambda, Amazon API Gateway, AWS Chatbot 등을 사용하여 Slack 또는 Microsoft Teams와 같은 협업 도구와 통합됩니다.

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
