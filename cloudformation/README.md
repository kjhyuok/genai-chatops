# CloudFormation 실행 방법

1. AWS Console > Cloudshell 실행합니다.

2. Workshop 코드를 다운로드 합니다.
```
git clone https://github.com/kjhyuok/genai-chatops.git
```

3. CloudFormation 실행합니다.
```
cd genai-chatops/cloudformation
chmod +x ./deploy.sh
./deploy.sh
```


# 실행 결과확인
1. AWS Console > CloudFormation 이동합니다.

2. chatops-stack 스택이 CREATE_COMPLETE 을 확인하고, Outputs 에서 API Gateway, S3 등 완성한 리소스를 확인할 수 있습니다.

![결과화면](./cloudformation_output.png)