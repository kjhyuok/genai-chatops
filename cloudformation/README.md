# CloudFormation 실행 방법


<details style="padding: 15px; border: 1px solid #d3d3d3; border-radius: 5px; margin: 10px 0;"> <summary style="font-size: 1em; font-weight: bold; color: #FFFFFF;">Windows 환경 설정 안내</summary>
deploy.sh 실행 시 zip 명령어가 필요한 경우, 다음 두 가지 방법 중 하나를 선택하여 설치하세요:

#### 방법 1: 관리자 권한으로 PowerShell 실행
1. 시작 메뉴에서 PowerShell 우클릭 > "관리자 권한으로 실행" 선택
2. 다음 명령어 실행:
```powershell
curl -O http://stahlworks.com/dev/zip.exe > C:/windows/system32/zip.exe
curl -O http://stahlworks.com/dev/unzip.exe > C:/windows/system32/unzip.exe
```
#### 방법 2: 수동 설치
1. http://stahlworks.com/dev/zip.exe 파일 직접 다운로드
   http://stahlworks.com/dev/unzip.exe 파일 직접 다운로드
2. 다운로드한 파일을 C:\Windows\System32 폴더에 관리자 권한으로 복사
</details>

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