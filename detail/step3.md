## Step 3: Log 모니터링 및 알림 메시지 수신을 위한 Slack 구성 및 AWS와 연동

### 목표
Slack 채널을 구성하고 AWS 서비스와 연동하여 로그 모니터링 및 알림 메시지를 수신합니다.

<img width="914" alt="image" src="https://github.com/user-attachments/assets/aa112901-6f33-415b-8b74-1b1714224631" />


### 실습 내용
1. Slack 계정을 신규로 생성하고, 워크스페이스와 채널을 만들기.
2. Amazon Q Developer in chat applications(구: AWS Chatbot)을 Slack에 배포.
3. Amazon Bedrock Agent와 Amazon Q Developer 와 연동.
   - 이 작업을 통해 Slack에서 Agent가 Amazon Bedrock에게 질의를 할 수 있게 됩니다.
4. Slack 채널에서 Amazon Bedrock 호출 테스트




---
## 1. Slack 계정을 신규로 생성하고, 워크스페이스와 채널을 만들기.<br>
본 Workshop에서 활용할 Slack을 무료버전으로 간단히 만들어 봅니다. (🚩업무에 불편을 주지 않을 Pure한 실습용 E-Mail로 만들어 주세요.)<br>
[Slack 가입하기](https://slack.com/intl/ko-kr/get-started?utm_source=google&utm_medium=paid_search&utm_campaign=kr__20241202&gclid=EAIaIQobChMI94iphN_YiwMVIeoWBR2xUx5bEAAYASAAEgLbJvD_BwE&campaign=701ed00000BwjL3AAJ&lpt=1#/createnew)

<img width="682" alt="image" src="https://github.com/user-attachments/assets/b5dd436d-15bb-4f0b-a370-7828d39f2641" />

워크스페이스를 생성합니다. 
<img width="898" alt="image" src="https://github.com/user-attachments/assets/f9ca58e6-4984-431b-88d7-af2f3897f250" />

고유한 이름이어야 하므로 ```aws-chatops-workshop-본인Alias지정``` 후 본인의 Alias 를 적당히 저장 합니다.
<img width="898" alt="image" src="https://github.com/user-attachments/assets/2b3fab17-b2f7-4ee7-933b-9086c578fc4c" />

무료플랜으로 생성 마무리 합니다.
<img width="898" alt="image" src="https://github.com/user-attachments/assets/f9f4fe2d-1c6d-4148-85e8-411028a44785" />

우리가 Amazon Bedrock과 소통할 채널을 생성해 줍니다. ```aws-chatops-workshop```
<img width="898" alt="image" src="https://github.com/user-attachments/assets/3583b50f-cbe8-41bf-a027-061440912674" />

성공적으로 새로운 Slack 워크스페이스(**aws-chatops-workshop-본인Alias지정**)를 생성하고, 새로운 채널(**aws-chatops-workshop**)까지 Web브라우저에서 완료했습니다.
<img width="898" alt="image" src="https://github.com/user-attachments/assets/75b966bf-0240-47e3-a05e-54f0014b27ac" />

## 2. Amazon Q Developer in chat applications(구: AWS Chatbot)을 Slack에 배포.<br>

자 이제 지금 생성한 Slack의 워크스페이스와 Step2에서 생성한 Amazon Bedrock Agent와의 Connector 역할을 수행할 Amazon Q Developer in chat applications 를 생성해 봅니다.
메뉴이동: [Amazon Q Developer in chat applications](https://us-east-2.console.aws.amazon.com/chatbot/home?region=us-west-2#/)

우측에서 채팅 클라이언트를 Slack으로 선택해주시고 클라이언트 구성선택을 해주세요.

<img width="898" alt="image" src="https://github.com/user-attachments/assets/77eb26df-2058-4aae-b4e7-d56ac07fae67" />

다음과 같이 Amazon Q Developer에서 Slack 워크스페이스에 액세스하기 위해 권한을 요청합니다.
<img width="898" alt="image" src="https://github.com/user-attachments/assets/517ba415-7eb5-4d6f-9d4a-7a0f6a61f9d1" />

우측 상단에 다른워크스페이스 추가 **+** 를 선택하시면, Slack 워크스페이스에 join할 수 있는 도메인을 입력하게 됩니다.<br>
여기서는 여러분이 앞서 생성해 놓은 워크스페이스를 입력해 주세요.<br>
워크스페이스의 Slack URL을 다음과 같이 복사해서 입력 > ```aws-chatops-workshop-본인Alias지정```
계속을 선택하고, Amazon Q Developer가 여러분 Slack 워크스페이스에 액세스 할 수있게 **허용** 해 줍니다.<br>
<img width="524" alt="image" src="https://github.com/user-attachments/assets/3d0da647-03ae-4425-8856-4d49aac3b965" />

가급적 여러분의 회사의 Slack과 불필요한 채널 혼용을 막기 위해 **꼭 Web브라우저**를 통해서 Slack에 접근해 주세요.<br>
이렇게 들어온 Slack에는 앞서 Amazon Q Developer in chat applications 을 통해서 생성했던 Amazon Q가 APP에 배포되어 있는 것을 확인 할 수 있습니다.<br>
<img width="1001" alt="image" src="https://github.com/user-attachments/assets/0c565eff-ce6f-4e46-b7a8-f22740bd55d5" />


## 3. Amazon Bedrock Agent와 Amazon Q Developer 와 연동.
Amazon Q Developer in chat applications(구: AWS Chatbot)은 Amazon Chime 이나 Slack과 연동하여 업무 자동화를 구현할 수 있는 서비스 입니다. 최근에는 Slack 과 연동한 AWS Chatbot과 Amazon Bedrock Agents와의 통합을 기점으로 더욱 손쉽게 Slack뿐만아니라 Microsoft Teams 채팅 채널에서 직접 Amazon Bedrock Agent와 상호작용이 가능하게 되어 기존에 비해 훨씬 심플하게 Amazon Bedrock과의 연동을 할 수 있게 되었습니다. 

이제 앞서 생성해서 Slack에 배포한 APP(이 Amazon Q Developer)을 Step2에서 구성한 Amazon Bedrock Agent와 연결해 보겠습니다.<br>
Agent와 연결을 위해서는 다음과 같은 설정이 필요합니다.

Amazon Q Developer in chat applications 메뉴에서 Slack WorkSpace: **aws-chatops-workshop-JK** 에 진입합니다.<br>
**새로운 채널 구성** 을 선택하여 환경설정을 해봅니다.
<img width="1273" alt="image" src="https://github.com/user-attachments/assets/bd8e0e73-db64-470d-bfc2-c929a0467add" />

**Configure Slack channel** 페이지에서는 Slack 채널의 속성, 이 Amazon Q Developer가 Bedrock을 Access 할 수 있는 IAM 역할과 Channel내 보안을 위한 가드레일 정책을 설정하게 됩니다. 이러한 가드레일 정책은 런타임 시 채널 IAM 역할과 사용자 역할 모두에 적용됩니다.<br>
> 설정을 위한 각 Field의 Value 아래에 정리해 둔 표를 참고하세요.
<img width="1273" alt="image" src="https://github.com/user-attachments/assets/d5f3a5cb-75f4-46b7-9037-623a00691502" />
<img width="1273" alt="image" src="https://github.com/user-attachments/assets/94254d76-c39d-4848-af59-f5ede6996a70" /><br>



| Field                   | Value                                                                                                                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Configuration details        | ```aws-chatops-workshop-2025```                                                                                                                                                                                                               |
| Slack channel(Public)     | ```aws-chatops-workshop-본인Alias지정```                                                                                                                                                                                                           |
| Permissions(Role settings)  | ```Channel role```선택                                                                                                                                                                                                                        |
| Permissions(Channel role)  | ```Use an existing IAM role```선택                                                                                                                                                                                                        |
| Permissions(Existing role)        | ```aws-chatops-workshop-role```선택                                                                                                                                                                                                          |
| Permissions(Policy name)        | ```ReadOnlyAccess```, ```AmazonBedrockFullAccess``` 2개 지정                                                                                                                                                                                            |

아래와 같이 성공적으로 채널구성을 완료했습니다. 
<img width="1514" alt="image" src="https://github.com/user-attachments/assets/a0256bf6-43a4-44fb-b2c4-aab97d5f52ec" />

앞서 만든 여러분의 Slack의 워크스페이스에 존재하는 채널: *#aws-chatops-workshop* 과 정상적인 연동이 되는지 진입해 보겠습니다. (*Channel > aws-chatops-workshop* 클릭!) 
<img width="1513" alt="image" src="https://github.com/user-attachments/assets/ef46add7-e5ad-4be8-bf3f-9e596e4cff66" />

정상적인 연동이 되었다면 앞서 접근했던 Slack 워크스페이스내의 aws-chatops-workshop 채널에 진입합니다.<br>
> Slack 데스크탑 APP으로 열지마시고, 되도록 브라우저를 통한 접근을 선택해 주세요.
<img width="1513" alt="image" src="https://github.com/user-attachments/assets/bb50d665-8e4a-4469-9843-34c8586ba063" />
<img width="1513" alt="image" src="https://github.com/user-attachments/assets/77de2012-f426-40e1-a5db-a470154399e5" />

배포하고 Guardrail policies 2개(ReadOnlyAccess, AmazonBedrockFullAccess)를 추가한 내용을 공유 드리며 자세한 설정방법은 Amazon Bedrock 에이전트 연결 설명서 페이지를 참조하세요.


이 작업을 통해 Slack에서 Agent가 Amazon Bedrock에게 질의를 할 수 있게 됩니다.


