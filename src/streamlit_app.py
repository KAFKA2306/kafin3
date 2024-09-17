import os
import io
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
import openai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Google Drive APIのスコープ
SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = 'token.json'

# OpenAI API setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Google Drive 認証情報のセットアップ
def setup_google_drive_service():
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
            drive_service = build('drive', 'v3', credentials=creds)
            return drive_service
        except RefreshError:
            st.error("認証情報の更新に失敗しました。token.jsonファイルを再作成してください。")
            return None
    else:
        st.error("token.jsonファイルが見つかりません。Google Cloud Consoleで認証情報を作成し、ダウンロードしてください。")
        return None

# ページ設定
st.set_page_config(page_title="KaFin2: AI-Powered Finance Dashboard", page_icon="🤖📊", layout="wide")

# タイトルと説明
st.title("KaFin2: AI-Powered Finance Dashboard 🤖📊")
st.write("Welcome to KaFin2, your AI-powered finance analysis tool!")

# セッション状態の初期化
if 'saved_tickers' not in st.session_state:
    st.session_state.saved_tickers = []

# 株式データを取得する関数
@st.cache_data
def get_stock_data(ticker, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# データをGoogle Driveに保存する関数
def save_to_google_drive(drive_service, ticker, data):
    try:
        file_metadata = {'name': f'{ticker}_data.csv'}
        media = MediaIoBaseUpload(io.StringIO(data.to_csv(index=True)),
                                  mimetype='text/csv',
                                  resumable=True)
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        file_id = file.get('id')
        return file_id
    except HttpError as error:
        st.error(f"Google Driveへのアップロード中にエラーが発生しました: {error}")
        return None

# ChatGPTを使用して分析を行う関数
def analyze_with_chatgpt(query, data):
    prompt = f"以下の株価データに基づいて、{query}について分析してください:\n\n{data.to_string()}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial analyst AI."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

# Google Driveサービスの初期化
drive_service = setup_google_drive_service()

# メインコンテンツ
tab1, tab2 = st.tabs(["Algorithmic Analysis", "Chat-based Analysis"])

with tab1:
    st.header("Algorithmic Analysis")
    
    # サイドバーでユーザー入力を受け取る
    st.sidebar.header("Analysis Parameters")
    ticker_input = st.sidebar.text_input("Enter stock ticker (e.g., AAPL, GOOGL)", "")
    days = st.sidebar.slider("Select number of days for analysis", 30, 365, 90)

    # 保存されたtickerの選択肢を表示
    saved_ticker = st.sidebar.selectbox("Or select a saved ticker", [''] + st.session_state.saved_tickers)

    # tickerの決定
    ticker = None  # 初期化

    if ticker_input:
        ticker = ticker_input.upper()  # 小文字を大文字に変換
        save_ticker = st.sidebar.checkbox("Save this ticker for future use")
        if save_ticker and ticker not in st.session_state.saved_tickers:
            st.session_state.saved_tickers.append(ticker)
    elif saved_ticker:
        ticker = saved_ticker

    # 株価分析を実行
    if ticker:
        # データ取得
        data = get_stock_data(ticker, days)
        
        if not data.empty:
            # Google Driveにデータを保存
            if drive_service:
                file_id = save_to_google_drive(drive_service, ticker, data)
                if file_id:
                    file_url = f"https://drive.google.com/file/d/{file_id}/view"
                    st.sidebar.write(f"Data saved to Google Drive. [View File]({file_url})")
                else:
                    st.sidebar.write("Google Driveへの保存に失敗しました。")

            # 株価チャートを表示
            st.subheader(f"{ticker} Stock Price - Last {days} Days")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index,
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'],
                            name='Price'))
            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # 基本統計量を表示
            st.subheader("Basic Statistics")
            st.write(data.describe())

            # リターンを計算して表示
            st.subheader("Returns Analysis")
            data['Daily Return'] = data['Close'].pct_change()
            st.write(f"Total Return: {(data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100:.2f}%")
            st.write(f"Average Daily Return: {data['Daily Return'].mean() * 100:.2f}%")
            st.write(f"Daily Return Volatility: {data['Daily Return'].std() * 100:.2f}%")
        else:
            st.write(f"No data available for {ticker}. Please check the ticker symbol or adjust the date range.")

with tab2:
    st.header("Chat-based Analysis")
    
    chat_ticker = st.text_input("Enter stock ticker for chat-based analysis", "")
    chat_days = st.number_input("Number of days for analysis", min_value=1, max_value=365, value=90)
    user_query = st.text_area("Enter your analysis request", "Analyze the trend and provide insights on the stock performance.")
    
    if st.button("Analyze with AI"):
        if chat_ticker:
            chat_data = get_stock_data(chat_ticker.upper(), chat_days)
            if not chat_data.empty:
                ai_analysis = analyze_with_chatgpt(user_query, chat_data)
                st.write(ai_analysis)
            else:
                st.write(f"No data available for {chat_ticker}. Please check the ticker symbol or adjust the date range.")
        else:
            st.write("Please enter a stock ticker for analysis.")

# サイドバーの追加情報
st.sidebar.markdown("---")
st.sidebar.write("This is an enhanced implementation of KaFin2 with both algorithmic and chat-based analysis capabilities.")

# メイン関数
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    stcli.main()
