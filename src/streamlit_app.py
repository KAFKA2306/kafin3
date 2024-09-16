import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import requests
import json

# ページ設定
st.set_page_config(page_title="KaFin2: AI-Powered Finance Dashboard", page_icon="🤖📊", layout="wide")

# タイトルと説明
st.title("KaFin2: AI-Powered Finance Dashboard 🤖📊")
st.write("Welcome to KaFin2, your AI-powered finance analysis tool!")

# サイドバーでユーザー入力を受け取る
st.sidebar.header("Analysis Parameters")
ticker = st.sidebar.text_input("Enter stock ticker (e.g., AAPL, GOOGL)", "AAPL")
days = st.sidebar.slider("Select number of days for analysis", 30, 365, 90)

# 株式データを取得する関数
@st.cache_data
def get_stock_data(ticker, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# データを取得
data = get_stock_data(ticker, days)

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

# サイドバーの追加情報
st.sidebar.markdown("---")
st.sidebar.write("This is a basic implementation of KaFin2. For more advanced features and AI-powered analysis, please refer to the full version.")

import streamlit.web.cli as stcli

# メイン関数
if __name__ == "__main__":
    
    stcli.main()
