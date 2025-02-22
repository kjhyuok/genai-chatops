# Step 1: IT운영팀의 업무자산을 Amazon Bedrock Knowledge Bases로 구성

### 목표
Amazon Bedrock Knowledge Bases를 활용하여 IT 운영팀의 업무 자산을 구성하고, Retrieval-Augmented Generation(RAG) 워크플로를 설정합니다.<br>

<img width="720" alt="image" src="https://github.com/user-attachments/assets/93c4366a-ead9-4524-bbd2-9e9141ec3b0e" /><br>


### 👉🏻이 Workshop의 모든 실습을 us-west-2(Oregon)에서 진행되니 AWS Console 우측 상단의 Region을 확인해 주세요.

## 실습 내용
1. Amazon Bedrock 메뉴에서 Knowledge Base 생성하기.
2. IT 운영팀의 문서 및 데이터 업로드 (JSON, CSV, PDF 등 지원).
3. 데이터가 벡터 임베딩으로 변환되는 과정을 확인.
4. Knowledge Base를 테스트하여 업로드한 데이터에서 정확한 응답 생성 확인.

---
## 1. Amazon Bedrock 메뉴에서 Knowledge Base 생성하기.<br>
메뉴이동: [Amazon Bedrock Knowledge Bases](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/knowledge-bases)<br>

<img width="666" alt="image" src="https://github.com/user-attachments/assets/44d2a571-10d2-4e97-8925-23f23cc8da05" />

1. 페이지에서 Knowledge Bases를 클릭하고 Create(선택: Create knowledge base with vector store)  <br>
Knowledge Base name 에는 ```knowledge-base-quick-start-2025``` 를 넣어줍니다.<br>
2. Data source 선택 후 Next<br>
Data source details > Choose data source 에서 **Amazon S3 를 데이터 소스로 선택**합니다.<br>
(현재 라디오버튼으로 1개만 선택되니 참고! 여러개 data source 선택시 기존 스텝 완료 후 가능)<br>
Data source name 에는 `knowledge-base-quick-start-ds-s3` 를 넣어줍니다.<br>
S3 URI는 자동 생성된 S3 Bucket을 Browse S3 버튼을 통해서 선택합니다. **chatops-kb-ds-2025** 선택
3. Parsing strategy<br>
다음은 Parsing 옵션을 선택하는데 데이터 처리 방법을 구성해야 합니다.(Knowledge Bases 생성 후에는 옵션수정 불가)<br>
**Amazon Bedrock default parser:** 기본 파서데이터의 텍스트만 처리하려면 **이 옵션을 선택** (요금이 발생X) Workshop에서는 이것을 선택<br>
**Amazon Bedrock Data Automation as parser:** 시각적으로 풍부한 문서 또는 이미지를 처리하려면 이 옵션을 선택(관리형 서비스)<br>
**Foundation models as a parser:** 시각적으로 풍부한 문서 또는 이미지를 처리.<br>
4. Chunking strategy > **디폴트 청킹** 을 선택 후 Next
5. Embeddings model > **Titan Text Embeddings V2** 선택 후 Apply
6. Vector database > Vector store > **Amazon OpenSearch Serverless** 선택 후 Next
7. Review 후 최종 생성
> 최종 생성까지는 약 3\~4분이 소요됩니다.
8. 
3. ㅇㅇ

4. ㅇㄹ
5. ㅇㄹ
6. ㅇㄹ
7. ㅇ
8. ㄹ

