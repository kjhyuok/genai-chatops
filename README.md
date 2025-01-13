# AWS 기반 ChatOps 프로젝트

AWS를 활용하여 ChatOps 환경을 구축하고 관리하기 위한 프로젝트입니다. 이 프로젝트는 AWS Lambda, Amazon API Gateway, AWS Chatbot 등을 사용하여 Slack 또는 Microsoft Teams와 같은 협업 도구와 통합됩니다.

---

## 📋 목차
1. [프로젝트 소개](#프로젝트-소개)
2. [아키텍처 개요](#아키텍처-개요)
3. [필수 조건](#필수-조건)
4. [설치 및 설정](#설치-및-설정)
5. [사용 방법](#사용-방법)
6. [기여 방법](#기여-방법)
7. [라이선스](#라이선스)

---

## 프로젝트 소개

이 프로젝트는 ChatOps를 통해 운영 활동을 중앙화하고, AWS 리소스와 상호작용하며 알림 및 명령 실행을 지원합니다. 주요 기능은 다음과 같습니다:
- AWS 이벤트에 대한 실시간 알림 전송
- Slack 또는 Microsoft Teams에서 명령 실행
- DevOps 및 운영 워크플로우 간소화
  
![image](https://github.com/user-attachments/assets/f3010c15-238e-4753-93cd-c397c3519a2e)

---

## 아키텍처 개요

아래는 이 프로젝트의 기본 아키텍처입니다:
![image](https://github.com/user-attachments/assets/4a45f49c-8924-4527-92e6-a613364e96c0)


1. **AWS Lambda**: Slack 또는 Teams의 요청을 처리.
2. **Amazon API Gateway**: Lambda 함수와 통신하는 HTTP 엔드포인트 제공.
3. **AWS Chatbot**: 알림 및 명령 처리를 위한 Slack/Teams 통합.
4. **Amazon SNS**: 알림 메시지 전송.
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
