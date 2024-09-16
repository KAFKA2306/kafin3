from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

# クライアントシークレットJSONファイルのパス (修正: エスケープシーケンス対応)
CLIENT_SECRETS_FILE = r"C:\secret\client_secret_659942893881-jtcrs4ckeip72u30bdbau2hfcp4ktfci.apps.googleusercontent.com.json"
# 必要なスコープ
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    # OAuth 2.0フローの初期化
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )
    
    # ローカルサーバーを使ってユーザーの認証を行う
    flow.run_local_server(port=0)
    
    # 認証情報を取得
    credentials = flow.credentials
    
    # token.jsonに認証情報を保存
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

    print("token.json has been created successfully.")

if __name__ == '__main__':
    main()
