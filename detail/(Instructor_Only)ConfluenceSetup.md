### Confluence Setup
Confluence는 이 Workshop에서 2가지 용도로 활용 됩니다.<br>
a. IT운영 자산이 등록되어 있다고 가정하고, Amazon Bedrock Knowledge Bases에 임베딩 후 RAG에 활용<br>
b. Slack Thread에 있는 내용을 Reporting되는 Space로 활용<br>

Lab4.AWS 서비스와 솔루션(Slack, Confluence)연결을 위해서 Workshop을 진행하시는 Instructor께서는 Atlassian Confluence(무료버전)에 가입해서 스페이스를 생성해 두고, 실습자들의 Amazon Bedrock을 활용한 Slack Thread 요약이 Reporting 될 수 있도록 사전에 준비해 주세요. 


1. [confluence 가입하기](https://www.atlassian.com/ko/software/confluence?gclsrc=aw.ds&&campaign=19190484181&adgroup=149977838531&targetid=kwd-22737151&matchtype=e&network=g&device=c&device_model=&creative=738967712140&keyword=confluence&placement=&target=&ds_eid=700000001542923&ds_e1=GOOGLE&gad_source=1&gclid=EAIaIQobChMIr6q2wt6SjAMVUMJMAh0rMBykEAAYASAAEgLIY_D_BwE)
<img width="1319" alt="image" src="https://github.com/user-attachments/assets/43d40e50-ed86-4231-bc56-908e7d7fb3e7" />

2. 무료 계정으로 가입 후 Site Domain 등록하기
<img width="670" alt="image" src="https://github.com/user-attachments/assets/e2c3be50-a7f9-4df8-a41b-ce1bf23cd178" />

등록 후 해당 Site에 대한 Confirm 메일을 수신합니다.
<img width="950" alt="image" src="https://github.com/user-attachments/assets/f384a817-a922-4fda-86a7-3a9ac89003e9" />

Confluence에 최초 진입 후 건너뛰기 > 완료 합니다.
<img width="1470" alt="image" src="https://github.com/user-attachments/assets/3a851e34-3b28-46a5-b3c6-c0f1f1ae81ad" />

3. 스페이스 생성하기
Slack Thread의 대화내용이나 장애내역이 요약되어 Reporting될 스페이스를 하나 생성합니다.
> ops_knowledge_bases 로 기재 합니다.

![image](https://github.com/user-attachments/assets/8383a180-2748-4d19-91be-f538b99cfa6f)

> 부가적인 기능을 모두 제거하고 생성합니다.

![image](https://github.com/user-attachments/assets/411df5bb-8a2c-4241-abe3-2b387f37a311)

> Reporting 게시글이 업로드 될 페이지를 하나 생성합니다. 임의로 _Issue reported from Slack_

![image](https://github.com/user-attachments/assets/93bc6ca1-b7b6-47ad-916e-1004d4180138)



3-1. 생성한 스페이스의 이름은 Workshop을 수행하는 분들의 자동생성된 Lambda(gw-to-slack)의 2곳과 동일해야 합니다.
**ops_knowledge_bases**_
![image](https://github.com/user-attachments/assets/48531582-7f8a-46ae-a63c-61d973c0be7d)
![image](https://github.com/user-attachments/assets/c5fd3a2d-a95e-4c59-a06e-32fa89bfae61)


3-2. 

3. Confluence에 Sample Reporting 등록하기
최초 생성된 Confluence에는 Amazon Bedrock Knowledge Bases에 임베딩 할만한 Reporting 자료가 없습니다. 실습 방법에 따라서 2가지의 방법이 사전에 필요합니다.<br>
   3-1. Instructor가 사전에 참조할 Sample Reporting 게시글을 아래에서 다운받아서 Confluence에 업로드 해 주시거나<br>
   SampleReporting Download 
   3-2. Amazon Bedrock Knowledge Bases를 S3로만 임베딩 하고 Reporting만 Confluence에 하시는 것을 권장 드립니다.<br>

5. 

6. 
