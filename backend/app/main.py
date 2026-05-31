from dotenv import load_dotenv
import os
from fastapi import FastAPI
import pandas as pd
from analytics import calculate_all
import psycopg2
load_dotenv()

app = FastAPI()

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
