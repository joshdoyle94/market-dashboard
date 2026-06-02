from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
import pandas as pd
from analytics import calculate_all
from fetch import fetch_prices, store_prices
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://market-dashboard-sooty.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "market dashboard API is running"}

@app.get("/prices")
def get_prices(ticker: str):
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    cursor = connection.cursor()

    cursor.execute(
            "SELECT MAX(date) AS most_recent_date FROM stock_data WHERE ticker = %s",
            (ticker,)
    )

    row = cursor.fetchone()
    latest_date = row[0]

    if latest_date is None:
        find_prices = fetch_prices([ticker], "1y")
        if not find_prices:
            raise HTTPException(status_code=404, detail="Ticker not found")
        else:
            store_prices(find_prices)
    else:
        # Freshness check relies on MAX(date) — detects staleness only at the
        # most-recent edge. Assumes contiguous data; does not detect interior
        # gaps, which can't occur in normal ingestion flow.
        today = date.today()
        gap = today - latest_date
        if gap.days > 2:
            find_prices = fetch_prices([ticker], "1y")
            store_prices(find_prices)
    

    df = pd.read_sql(
        "SELECT * FROM stock_data WHERE ticker = %s",
        connection,
        params=(ticker,)
    )

    result = calculate_all(df)
    serializable = {}
    for window, metrics in result.items():
        serializable[str(window)] = {
            "daily_returns": metrics["daily_returns"].dropna().tolist(),
            "moving_average": metrics["moving_average"].dropna().tolist(),
            "volatility": metrics["volatility"].dropna().tolist()
        }

    connection.close()
    return serializable
