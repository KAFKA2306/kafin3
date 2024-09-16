import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import yfinance as yf
import pandas as pd
import numpy as np
from fredapi import Fred
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import openai
from dotenv import load_dotenv
from datetime import datetime, timedelta
import joblib
from sklearn.ensemble import RandomForestRegressor

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API keys and configurations
openai.api_key = os.getenv("OPENAI_API_KEY")
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

class AnalysisRequest(BaseModel):
    query: str

class FinancialData(BaseModel):
    date: List[str]
    values: List[float]
    symbol: str

class AnalysisResponse(BaseModel):
    chartData: List[dict]
    aiAnalysis: str
    financialAnalysis: dict

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_financial_data(request: AnalysisRequest):
    try:
        # Use GPT-4 to interpret the user's query
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analysis assistant. Interpret the user's query and provide instructions for data retrieval and analysis."},
                {"role": "user", "content": request.query}
            ]
        )
        interpretation = gpt_response.choices[0].message.content

        # Extract relevant information from the GPT-4 interpretation
        # This is a simplified example; in practice, you'd need more sophisticated parsing
        if "stock" in interpretation.lower():
            symbol = interpretation.split()[-1]  # Assume the last word is the stock symbol
            data = get_stock_data(symbol)
        elif "fred" in interpretation.lower():
            series_id = interpretation.split()[-1]  # Assume the last word is the FRED series ID
            data = get_fred_data(series_id)
        else:
            raise ValueError("Unable to interpret the query")

        # Perform financial analysis
        analysis = perform_financial_analysis(data)

        # Generate AI analysis
        ai_analysis = generate_ai_analysis(data, analysis)

        # Prepare chart data
        chart_data = [{"date": date, "value": value} for date, value in zip(data.date, data.values)]

        return AnalysisResponse(
            chartData=chart_data,
            aiAnalysis=ai_analysis,
            financialAnalysis=analysis
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_stock_data(symbol: str) -> FinancialData:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    data = yf.download(symbol, start=start_date, end=end_date)
    return FinancialData(
        date=data.index.strftime('%Y-%m-%d').tolist(),
        values=data['Close'].tolist(),
        symbol=symbol
    )

def get_fred_data(series_id: str) -> FinancialData:
    data = fred.get_series(series_id)
    return FinancialData(
        date=data.index.strftime('%Y-%m-%d').tolist(),
        values=data.tolist(),
        symbol=series_id
    )

def perform_financial_analysis(data: FinancialData) -> dict:
    df = pd.DataFrame({"date": data.date, "value": data.values})
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    analysis = {
        "mean": np.mean(data.values),
        "std": np.std(data.values),
        "min": np.min(data.values),
        "max": np.max(data.values),
        "last_value": data.values[-1],
        "pct_change": (data.values[-1] / data.values[0] - 1) * 100
    }
    
    # Simple forecasting using Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    df['lag_1'] = df['value'].shift(1)
    df['lag_7'] = df['value'].shift(7)
    df.dropna(inplace=True)
    
    X = df[['lag_1', 'lag_7']]
    y = df['value']
    
    model.fit(X, y)
    
    last_known = df.iloc[-1]
    forecast_input = np.array([[last_known['value'], last_known['lag_7']]])
    forecast = model.predict(forecast_input)[0]
    
    analysis["forecast_next_day"] = forecast
    
    return analysis

def generate_ai_analysis(data: FinancialData, analysis: dict) -> str:
    prompt = f"""
    Analyze the following financial data and provide insights:
    Symbol: {data.symbol}
    Time period: {data.date[0]} to {data.date[-1]}
    Last value: {analysis['last_value']}
    Percent change: {analysis['pct_change']:.2f}%
    Mean: {analysis['mean']:.2f}
    Standard deviation: {analysis['std']:.2f}
    Forecast for next day: {analysis['forecast_next_day']:.2f}
    
    Please provide a concise analysis of this data, including potential factors influencing the trends and what it might mean for investors.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial analyst providing insights on market data."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)