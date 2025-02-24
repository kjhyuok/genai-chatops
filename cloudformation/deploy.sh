#!/bin/bash

# 변수 설정
STACK_NAME="chatops-stack"
AWS_REGION="us-west-2"

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
BUCKET_NAME="chatops-lambda-code-$AWS_ACCOUNT_ID"

echo $BUCKET_NAME

# 버킷 존재 여부 확인
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo "Bucket $BUCKET_NAME already exists"
else
    echo "Creating bucket $BUCKET_NAME"
    aws s3api create-bucket \
        --bucket $BUCKET_NAME \
        --region $AWS_REGION \
        --create-bucket-configuration LocationConstraint=$AWS_REGION

    if [ $? -eq 0 ]; then
        echo "Bucket created successfully"
    else
        echo "Failed to create bucket"
        exit 1
    fi
fi

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
    --capabilities CAPABILITY_NAMED_IAM \
    --region $AWS_REGION
