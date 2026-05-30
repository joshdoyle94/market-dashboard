import yfinance as yf
import psycopg2
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

# TO DO - move to config file later
connection = psycopg2.connect(
    dbname="market_dashboard",
    user="joshdoyle",
    password="",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()               # the thing you use to run SQL

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

result = fetch_prices(ticker=ticker_list, period="1y")

def store_prices(data):
    connection = psycopg2.connect(
        dbname="market_dashboard",
        user="joshdoyle",
        password="",
        host="localhost",
        port="5432"
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

store_prices(result)