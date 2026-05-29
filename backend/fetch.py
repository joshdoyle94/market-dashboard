import yfinance as yf
import sqlite3
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

connection = sqlite3.connect("market.db")  # creates the file if it doesn't exist
cursor = connection.cursor()               # the thing you use to run SQL

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_data (
        ticker TEXT NOT NULL,
        date TEXT,
        open REAL,
        close REAL,
        high REAL,
        low REAL,
        volume REAL
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

result = fetch_prices(ticker=ticker_list, period="5d")

def store_prices(data):
    connection = sqlite3.connect("market.db")
    cursor = connection.cursor()

    for ticker, df in data.items():
        for date, row in df.iterrows():
            cursor.execute("""
                INSERT INTO stock_data (ticker, date, open, high, low, close, volume)
                VALUES (:ticker, :date, :open, :high, :low, :close, :volume)
            """, {
                "ticker": ticker,
                "date": str(date),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            })

    connection.commit()
    connection.close()
    print("Rows inserted successfully")

store_prices(result)