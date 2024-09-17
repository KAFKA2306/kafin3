import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import yfinance as yf
import pandas as pd
import numpy as np
from fredapi import Fred
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API keys
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

class AnalysisRequest(BaseModel):
    query: str
    days: Optional[int] = 365

class FinancialData(BaseModel):
    dates: List[str]
    values: List[float]
    symbol: str

class AnalysisResponse(BaseModel):
    chartData: List[dict]
    statistics: dict

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_financial_data(request: AnalysisRequest):
    try:
        # Simple parsing of the query
        if "stock" in request.query.lower():
            symbol = request.query.split()[-1].upper()
            data = get_stock_data(symbol, request.days)
        elif "fred" in request.query.lower():
            series_id = request.query.split()[-1]
            data = get_fred_data(series_id, request.days)
        else:
            raise ValueError("Unable to interpret the query")

        analysis = perform_financial_analysis(data)
        chart_data = [{"date": date, "value": value} for date, value in zip(data.dates, data.values)]

        return AnalysisResponse(
            chartData=chart_data,
            statistics=analysis
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_stock_data(symbol: str, days: int) -> FinancialData:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = yf.download(symbol, start=start_date, end=end_date)
    return FinancialData(
        dates=data.index.strftime('%Y-%m-%d').tolist(),
        values=data['Close'].tolist(),
        symbol=symbol
    )

def get_fred_data(series_id: str, days: int) -> FinancialData:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = fred.get_series(series_id, start_date, end_date)
    return FinancialData(
        dates=data.index.strftime('%Y-%m-%d').tolist(),
        values=data.tolist(),
        symbol=series_id
    )

def perform_financial_analysis(data: FinancialData) -> dict:
    values = np.array(data.values)
    
    analysis = {
        "mean": np.mean(values),
        "std": np.std(values),
        "min": np.min(values),
        "max": np.max(values),
        "last_value": values[-1],
        "pct_change": (values[-1] / values[0] - 1) * 100 if len(values) > 1 else 0
    }
    
    return analysis

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
