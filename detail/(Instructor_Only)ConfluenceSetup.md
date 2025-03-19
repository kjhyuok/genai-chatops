### Confluence Setup
Confluence는 이 Workshop에서 2가지 용도로 활용 됩니다.<br>
a. IT운영 자산이 등록되어 있다고 가정하고, Amazon Bedrock Knowledge Bases에 임베딩 후 RAG에 활용<br>
b. Slack Thread에 있는 내용을 Reporting되는 Space로 활용<br>

Lab4.AWS 서비스와 솔루션(Slack, Confluence)연결을 위해서 Workshop을 진행하시는 Instructor께서는 Atlassian Confluence(무료버전)에 가입해서 스페이스를 생성해 두고, 실습자들의 Amazon Bedrock을 활용한 Slack Thread 요약이 Reporting 될 수 있도록 사전에 준비해 주세요.(약 15분의 사전준비과정)
실습을 위해 아래를 준비하여 실습에 참여한 분들께 제공해 드려야 합니다:
- 실습용 Atlassian Confluence 무료버전 생성(URL, ID, PW)
- 스페이스와 페이지 생성(페이지ID)
- API 토큰 발급(API 토큰값)


1. [confluence 가입하기](https://www.atlassian.com/ko/software/confluence?gclsrc=aw.ds&&campaign=19190484181&adgroup=149977838531&targetid=kwd-22737151&matchtype=e&network=g&device=c&device_model=&creative=738967712140&keyword=confluence&placement=&target=&ds_eid=700000001542923&ds_e1=GOOGLE&gad_source=1&gclid=EAIaIQobChMIr6q2wt6SjAMVUMJMAh0rMBykEAAYASAAEgLIY_D_BwE)
<img width="1319" alt="image" src="https://github.com/user-attachments/assets/43d40e50-ed86-4231-bc56-908e7d7fb3e7" />

- 무료 계정으로 가입 후 Site Domain 등록하기
<img width="670" alt="image" src="https://github.com/user-attachments/assets/e2c3be50-a7f9-4df8-a41b-ce1bf23cd178" />

- 등록 후 해당 Site에 대한 Confirm 메일을 수신합니다.
<img width="950" alt="image" src="https://github.com/user-attachments/assets/f384a817-a922-4fda-86a7-3a9ac89003e9" />

- Confluence에 최초 진입 후 건너뛰기 > 완료 합니다.
<img width="1470" alt="image" src="https://github.com/user-attachments/assets/3a851e34-3b28-46a5-b3c6-c0f1f1ae81ad" />

2. 스페이스와 페이지 생성하기
Slack Thread의 대화내용이나 장애내역이 요약되어 Reporting될 스페이스를 하나 생성합니다.
- issuehistory 로 기재하며, 스페이스 키 역시 동일하게 issuehistory 로 입력 합니다. 이 스페이스 키 값은 Workshop에서 자동생성된 Lambda(chatops-stack-gw-to-slack-function)에 2곳에 동일하게 이미 입력되어 있습니다.
![image](https://github.com/user-attachments/assets/6345ac02-3dce-4035-b4e1-21e3dbfb8303)
![image](https://github.com/user-attachments/assets/95abbbb8-ffb5-4fea-8f95-b15e5de88d1b)


<img width="1283" alt="image" src="https://github.com/user-attachments/assets/68d7f1b1-5af5-4cc2-86e5-09ba0c208a66" />


> 부가적인 기능을 모두 제거하고 생성합니다.

![image](https://github.com/user-attachments/assets/411df5bb-8a2c-4241-abe3-2b387f37a311)

> Reporting 게시글이 업로드 될 페이지를 하나 생성합니다. 임의로 Issue reported from Slack

![image](https://github.com/user-attachments/assets/2d4190d6-fa6d-42f8-ab06-ffb6fb8bc6f6)
![image](https://github.com/user-attachments/assets/59b515ff-b61d-41ed-a019-06ebffe7a53a)

이제 Workshop에서 생성하는 Reporting 이 페이지에 게시 됩니다.
페이지가 생성되면 URL내의 페이지 ID(숫자형식)를 확보하여 Workshop에서 자동생성된 Lambda(chatops-stack-gw-to-slack-function)에 replace 할 수 있도록 합니다.
이 작업은 Workshop 참가자에게 안내해 주시고, Lab4-3.AWS Lambda(chatops-stack-gw-to-slack-function) 진행중에 반영합니다.

![image](https://github.com/user-attachments/assets/c4042138-f80d-45ed-9b9a-865339d4be87)
![image](https://github.com/user-attachments/assets/771ead98-49c8-432c-97ff-ed238fab02a5)


---
3. api-token 발급하기
api-token 값은 모두 AWS Secrets Manager에 Secret value 로 저장되며, 다음을 위해서 필요합니다.
a. Workshop 참가자들이 Amazon Bedrock Knowledge Bases 에 DataSource로 등록하고 Sync 하기 위해
b. Workshop 참가자들이 Instructor의 Confluence를 활용하여 Reporting을 생성하기 위해

[1.Confluence API 토큰](http://id.atlassian.com/manage-profile/security/api-tokens) 접속

API토큰 만들기 버튼으로 토큰을 생성합니다.
![image](https://github.com/user-attachments/assets/1f9f8a53-66a6-4cf2-b1e0-71c6c5bab2c0)

만료일자는 최대 1년입니다.
![image](https://github.com/user-attachments/assets/fcf19c6d-1053-444b-913c-2640eac5303e)

생성된 API 토큰을 복사해 둡니다.
![image](https://github.com/user-attachments/assets/0ce73d63-be43-45b1-b97c-a11c810b38a5)

Workshop 참가자들이 다수일 경우 이 API토큰을 넉넉하게 만들어서 배포합니다.(SPEC: 최대 25개)
여러개를 만들어 배포하는 이유는 Workshop 참가자들이 Amazon Bedrock Knowledge Bases 에 DataSource로 등록하고 Sync 하기 위해 동시에 접근 시 Fail이 발생할 수 있습니다.
![image](https://github.com/user-attachments/assets/04b4013c-85e6-495b-8f8f-6e540cebc671)






스페이스를 만들었고 Reporting 이 게시될 페이지를 만들었는데



3-1. 생성한 스페이스의 이름은 Workshop을 수행하는 분들의 자동생성된 Lambda(gw-to-slack)의 2곳과 동일해야 합니다.


3-2. 

3. Confluence에 Sample Reporting 등록하기
최초 생성된 Confluence에는 Amazon Bedrock Knowledge Bases에 임베딩 할만한 Reporting 자료가 없습니다. 실습 방법에 따라서 2가지의 방법이 사전에 필요합니다.<br>
   3-1. Instructor가 사전에 참조할 Sample Reporting 게시글을 아래에서 다운받아서 Confluence에 업로드 해 주시거나<br>
   SampleReporting Download 
   3-2. Amazon Bedrock Knowledge Bases를 S3로만 임베딩 하고 Reporting만 Confluence에 하시는 것을 권장 드립니다.<br>

5. 

6. 
