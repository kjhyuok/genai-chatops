# Step 1: IT운영팀의 업무자산을 Amazon Bedrock Knowledge Bases로 구성

### 목표
Amazon Bedrock Knowledge Bases를 활용하여 IT 운영팀의 업무 자산을 구성하고, Retrieval-Augmented Generation(RAG) 워크플로를 설정합니다.<br>

<img width="720" alt="image" src="https://github.com/user-attachments/assets/93c4366a-ead9-4524-bbd2-9e9141ec3b0e" /><br>


>👉🏻이 Workshop의 모든 실습을 us-west-2(Oregon)에서 진행되니 AWS Console 우측 상단의 Region을 확인해 주세요.

## 실습 내용
1. Amazon Bedrock 메뉴에서 Knowledge Base 생성하기.
2. IT 운영팀의 문서 및 데이터 업로드 (JSON, CSV, PDF 등 지원).
3. 데이터가 벡터 임베딩으로 변환되는 과정을 확인.
4. Knowledge Base를 테스트하여 업로드한 데이터에서 정확한 응답 생성 확인.

---
## 1. Amazon Bedrock 메뉴에서 Knowledge Base 생성하기.<br>
메뉴이동: [Amazon Bedrock Knowledge Bases](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/knowledge-bases)<br>

![](https://static.us-east-1.prod.workshops.aws/public/88811a7e-410e-4614-835d-b5bdc1092470/static/images/kb_details.gif)


<img width="666" alt="image" src="https://github.com/user-attachments/assets/44d2a571-10d2-4e97-8925-23f23cc8da05" /> 

**1. 페이지에서 Knowledge Bases를 클릭하고 Create<br>**
- (선택: Create knowledge base with vector store) <br>
- Knowledge Base name 에는 ```knowledge-base-quick-start-2025``` 를 넣어줍니다.<br>

**2. Data source 선택 후 Next**(🚩**S3를 Data source 선택하기**)<br>
- Data source details > Choose data source 에서 **Amazon S3 를 데이터 소스로 선택**합니다.<br>
- (현재 라디오버튼으로 1개만 선택되니 참고! 여러개 data source 선택시 기존 스텝 완료 후 가능)<br>
- Data source name 에는 `knowledge-base-quick-start-ds-s3` 를 넣어줍니다.<br>
- S3 URI는 자동 생성된 S3 Bucket을 Browse S3 버튼을 통해서 선택합니다. **chatops-kb-ds-2025** 선택

**3. Parsing strategy<br>**
- 다음은 Parsing 옵션을 선택하는데 데이터 처리 방법을 구성해야 합니다.(Knowledge Bases 생성 후에는 옵션수정 불가)<br>
**Amazon Bedrock default parser:** 기본 파서데이터의 텍스트만 처리하려면 **이 옵션을 선택** (요금이 발생X) Workshop에서는 이것을 선택<br>
**Amazon Bedrock Data Automation as parser:** 시각적으로 풍부한 문서 또는 이미지를 처리하려면 이 옵션을 선택(관리형 서비스)<br>
**Foundation models as a parser:** 시각적으로 풍부한 문서 또는 이미지를 처리.<br>

**4. Chunking strategy**
- **디폴트 청킹** 을 선택 후 Next

**5. Embeddings model**
- **Titan Text Embeddings V2** 선택 후 Apply

**6. Vector database**
- Vector store > **Amazon OpenSearch Serverless** 선택 후 Next

**7. Review 후 최종 생성**
> 최종 생성까지는 약 3\~4분이 소요됩니다.

🚩**Atlassian Confluence를 Data source 선택하기**<br>
앞서 Knowledge Bases를 최초 생성하는 과정에서 Amazon S3를 Data source 로 추가한 바 있습니다.<br> 
이번에는 팀내 협업 도구로 많이들 활용하시는 Atlassian Confluence를 Data source 로 추가해 보겠습니다.

이 설정에서는 Amazon Knowledge Bases 와 Atlassian Confluence 간의 Authentication이 필요합니다. 
이 과정에서 Authentication method 로 Basic Authentication 을 선택하게 되는데 안전한 인증을 위해 AWS Secrets Manager Secret 의 ARN을 통해서 진행합니다.
따라서 이 인증을 위해서 AWS Secrets Manager Secret 를 미리 생성해 보겠습니다. 
원활한 Workshop을 위해 강사가 제공하는 아래의 정보(Atlassian Confluence 인증키)를 참고해서 Secret 생성해 주세요.

**Secret Manager Screts 생성하기**
메뉴이동: [AWS Secrets Manager](https://us-west-2.console.aws.amazon.com/secretsmanager/landing?region=us-west-2)<br>

Choose secret type: **Other type of secret** 선택
Key/value pairs
| Key                   | Value                                                                                                                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| username        | ```강사가 제공```                                                                                                                                                                                                               |
| password        | ```강사가 제공```                                                                                                                                                                                                                        |

[Secret name and description 은 아래와 같이 입력하고 Next로 생성완료]<br>
Secret name: **```AmazonBedrock-DataStore-Secret```**<br>
Secret description: **```Confluence-Wiki```**<br>
<img width="1109" alt="image" src="https://github.com/user-attachments/assets/699f016b-6dad-478c-8356-3dde73bc9282" />







1. Knowledge Base 메뉴에서 이전 단계에서 생성이 완료된 **knowledge-base-quick-start-2025** 로 진입합니다.
2. Data source > Add > Third party data sources 에서 **Confluence** 를 선택하고 Next
3. Name에는 ```knowledge-base-quick-start-ds-Confluence``` 라고 입력합니다.
4. Source > Confluence URL 에는 강사가 제공하는 아래를 참고하세요.
```https://aws-chatops-workshop.atlassian.net```
5. Authentication(Authentication method) > Basic Authentication
⭐️⭐️⭐️AWS Secrets Manager secret 이 부분 선행 필요!!⭐️⭐️⭐️
ARN 정보 입력하기
7. Content chunking and parsing(Parsing strategy)
Amazon Bedrock default parser

<img width="990" alt="image" src="https://github.com/user-attachments/assets/89173112-2e09-46ef-ade4-4fcb7f0cf9a6" />

9. 순차적인 sync
<img width="816" alt="image" src="https://github.com/user-attachments/assets/e28733e6-374e-4ef7-88d3-ef1f9f69428f" />
<img width="816" alt="image" src="https://github.com/user-attachments/assets/0cafddcd-9cc1-476d-a3ce-3a67875abaa9" />


> 2개의 Data Source 최초 sync까지는 약 10분\~20분이 소요됩니다. **Break Time**

11. dfd
12. 











