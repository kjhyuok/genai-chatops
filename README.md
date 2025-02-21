![image](https://github.com/user-attachments/assets/30a81c3b-8356-4cd4-9686-14c38bf57218)# 🤖AWS GenAI를 활용한 IT 서비스 운영 자동화

현대의 IT 인프라 환경은 그 규모와 복잡성이 기하급수적으로 증가하고 있습니다. 클라우드 네이티브 아키텍처의 도입이나 마이크로서비스 기반 애플리케이션의 확산으로 기업의 IT 운영팀이 대응해야 할 영역은 지속적으로 확장되고 있습니다. 특히 시스템 전반에서 발생하는 다양한 종류의 로그 데이터, 메트릭 그리고 메시지들을 효과적으로 분석하고 신속하게 대응하는 것이 중요한 과제로 떠오르고 있습니다. 
1. 신속한 장애 대응의 필요성
특히 운영중인 시스템에 장애가 발생할 경우, IT운영팀은 해당 원인을 신속히 파악하고 해결해야 하는데, 시스템 규모 그리고 아키텍처 복잡성으로 인해 증가된 정보는 에러 메시지 발생시 빠르게 근본 원인을 식별하기가 어렵습니다. 게다가 다양한 연관 솔루션을 운영한다면 IT운영팀의 부담은 더욱 가중됩니다.
2. 지식의 자산화 필요성
또한 장애가 해결된 이후에도 동일한 문제 발생 시 과거의 경험을 바탕으로 보다 빠르고 효율적으로 해결할 수 있다면 IT운영팀의 축적된 장애 대응 경험과 해결 노하우가 매우 중요한 자산입니다. 그래서 우리는 이러한 정보를 잘 요약된 내용으로 정리하여 추후 장애 시 활용한다면 장애의 빈도가 높은 모듈에 대한 개선 그리고 업무의 효율성을 높일 수 있습니다.

---

## 📋 목차
1. [Workshop 소개](#Workshop-소개)
2. [아키텍처 개요](#아키텍처-개요)
3. [필수 조건](#필수-조건)
4. [설치 및 설정](#설치-및-설정)
5. [사용 방법](#사용-방법)

---

## Workshop 소개: 생성형 AI 기반 문제 분석 및 활용

이 Workshop에서는 위와 같은 문제를 지원하기 위해 AWS의 생성형 AI서비스와 기업에서 주로 활용중인 협업 도구인 Slack, Atlassian Confluence를 통합한 생성형 AI 기반 클라우드 운영 지원 솔루션을 소개할 예정입니다. 솔루션은 아래 그림과 같이 총 3개의 주요한 흐름으로 구성되어 있습니다.
1. Slack에서의 협업 및 문제 해결(①,②,③,④,⑤)
2. 분석 된 문제를 요약 후 게시글 생성(⑥)
3. 지속적인 학습 및 개선활용(⑦)
  
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/e568b940-b637-4421-add3-311c6c020d85" />

---

## Workshop의 결과물: 

이 Workshop을 완료하면 다음과 같이 IT서비스 운영에 활용되는 Usecase를 경험해 볼 수 있습니다.

Usecase 1 : 운영중 수신되는 Error Message에 대한 빠른 분석
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/442c812a-98de-48b7-8e1e-6aa33da3af79" />

Usecase 2 : Knowledge Bases 를 통한 문제의 근본 원인 분석 및 해결 방안 제시
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/a5466e02-aeb8-40c0-93c5-025fbe60deb2" />

Usecase 3 : 분석이 완료된 내용을 Wiki에 등록하고 팀의 자산화
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/a21f8fce-9c7a-49f0-8d15-df25cf3b0014" />

## 전체 아키텍처 및 흐름

아래는 이 프로젝트의 기본 아키텍처입니다:

<img width="1474" alt="image" src="https://github.com/user-attachments/assets/3115ef37-a187-4d18-9f18-7c6b7b8e709f" />
<img width="1474" alt="image" src="https://github.com/user-attachments/assets/2b2e3c82-7712-435d-976f-e4ae648a0237" />

단계 1: Knowledge Bases 구성
단계 2: 로그 모니터링 및 알림 전송
단계 3: 이슈 분석
단계 4: 분석내용의 등록 및 자산화

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
