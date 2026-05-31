from dotenv import load_dotenv
import os
import yfinance as yf
import psycopg2
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
load_dotenv()

def init_db():
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            ticker TEXT NOT NULL,
            date DATE,
            open DOUBLE PRECISION,
            close DOUBLE PRECISION,
            high DOUBLE PRECISION,
            low DOUBLE PRECISION,
            volume DOUBLE PRECISION
        )
    """)
    connection.commit()
    connection.close()

ticker_list = ["TSLA", "AAPL", "NVDA", "BIRDDDDD", "NFLX"]


def fetch_prices(ticker, period):
    stock_data = {}
    for x in ticker:
        stock = yf.Ticker(x)
        data = stock.history(period)

        if not data.empty:
            stock_data[x] = data
    return stock_data

def store_prices(data):
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = connection.cursor()

    for ticker, df in data.items():
        for date, row in df.iterrows():
            cursor.execute("""
                INSERT INTO stock_data (ticker, date, open, high, low, close, volume)
                VALUES (%(ticker)s, %(date)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s)
            """, 
                {
                    "ticker": ticker,
                    "date": date.date(),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": float(row["Volume"])
                })

    connection.commit()
    connection.close()
    print("Rows inserted successfully")

if __name__ == "__main__":
    init_db()
    result = fetch_prices(ticker_list, "1y")
    store_prices(result)