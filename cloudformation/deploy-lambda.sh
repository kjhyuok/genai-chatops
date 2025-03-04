#!/bin/bash

# 변수 설정
GITHUB_REPO="https://github.com/kjhyuok/genai-chatops"
LOCAL_DIR="genai-chatops"
LAMBDA_FUNCTION_NAME_1="chatops-gw-to-slack-function"
LAMBDA_FUNCTION_NAME_2="chatops-msg-to-slack-function"
REGION="us-east-1"  # AWS 리전

# 1. GitHub에서 소스 클론
echo "Cloning repository from GitHub..."
git clone $GITHUB_REPO $LOCAL_DIR
cd $LOCAL_DIR
cd cloudformation

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