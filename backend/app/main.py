from fastapi import FastAPI
import pandas as pd
from analytics import calculate_all
import psycopg2

app = FastAPI()

@app.get("/")
def root():
    return {"message": "market dashboard API is running"}

@app.get("/prices")
def get_prices(ticker: str):
    connection = psycopg2.connect(
        dbname="market_dashboard",
        user="joshdoyle",
        password="",
        host="localhost",
        port="5432"
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
