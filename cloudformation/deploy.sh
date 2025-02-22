#!/bin/bash

# 변수 설정
STACK_NAME="chatops-stack"
AWS_REGION="ap-northeast-2"

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
BUCKET_NAME="chatops-lambda-code-$AWS_ACCOUNT_ID"

echo $BUCKET_NAME

# S3 버킷 생성 (없는 경우)
aws s3api create-bucket \
    --bucket $BUCKET_NAME \
    --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_REGION

# Lambda 코드 ZIP 파일 생성
cd lambda-gw-to-slack
echo "Compressing lambda-gw-to-slack..."
find . -type f -print | zip -rv ../lambda-gw-to-slack.zip -@
cd ..

cd lambda-message-to-slack
echo "Compressing lambda-message-to-slack..."
find . -type f -print | zip -rv ../lambda-message-to-slack.zip -@
cd ..

aws s3 cp lambda-gw-to-slack.zip s3://$BUCKET_NAME/
aws s3 cp lambda-message-to-slack.zip s3://$BUCKET_NAME/

# CloudFormation 스택 배포
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        S3BucketLambdaCode=$BUCKET_NAME \
    --capabilities CAPABILITY_IAM
