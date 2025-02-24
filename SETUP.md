# 실습 사전 구성 가이드

이 문서는 실습 환경을 준비하는 과정을 단계별로 설명합니다.


## Step 1. 실습 계정 접속

1. **이메일 OTP 인증 선택**

   ![image](https://github.com/user-attachments/assets/8bdaf9d8-18a8-4f35-9db8-c71b86b7014c)


3. **이메일로 전송된 Passcode 입력**

   ![image](https://github.com/user-attachments/assets/94f045f2-173b-44c3-ac70-e9372d19b8de)

5. **AWS 콘솔 열기**

   좌측 하단의 **Open AWS console** 버튼을 클릭하여 실습 계정으로 이동합니다.

   <img width="980" alt="image" src="https://github.com/user-attachments/assets/8ad565eb-df82-46a8-8ea1-0a69e60670ef" />

> 🚩반드시 **Oregon (us-west-2) 리전** 을 확인합니다.

## Step 2. Bedrock 초기 설정

1. [Bedrock 콘솔](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/)로 이동합니다.

2. 좌측 탭 하단의 **Model access** 버튼을 클릭하거나, 이 [링크](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)를 통해 이동합니다.

3. Amazon 전체 모델과 Anthropic 모델 중 Claude 3.5 Sonnet 을 선택하고, 하단의 **Save changes** 버튼을 누릅니다.
 <img width="780" alt="image" src="https://github.com/user-attachments/assets/72c6b276-5201-4dde-b313-b84cff0a0eb9" />

4. 잠시 후 모델의 Access status가 `Access granted`로 변경됩니다.

이제 AWS Workshop Account에 진입하여, Bedrock 모델 활성화 까지 완료 했습니다.<br>
Workshop을 위한 기본적인 준비가 완료되었습니다.<br>

본 Workshop에서 활용되는 서비스는 다양하기 때문에 AWS Cloudformation을 통해서 몇가지 AWS Resource를 자동으로 생성하고 시작합니다.<br>
- AWS Lambda
- Amazon S3
- Amazon API Gateway

---

이제 AWS Cloudformation 수행을 위한 [Preparations](cloudformation/README.md) 으로 이동!
