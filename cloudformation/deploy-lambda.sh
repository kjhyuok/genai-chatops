#!/bin/bash

# 변수 설정
LAMBDA_FUNCTION_NAME_1="chatops-gw-to-slack-function"
LAMBDA_FUNCTION_NAME_2="chatops-msg-to-slack-function"
REGION="us-west-2"  # AWS 리전

# 2. Lambda 함수 코드 업데이트
echo "Updating Lambda function code..."
aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION_NAME_1 \
    --zip-file fileb://lambda-gw-to-slack.zip \
    --region $REGION

aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION_NAME_2 \
    --zip-file fileb://lambda-message-to-slack.zip \
    --region $REGION

echo "Deployment completed successfully!"