# Market Dashboard

A full-stack market data dashboard that ingests equity price data, stores it in
PostgreSQL, computes financial analytics, and serves them through a REST API to an
interactive React frontend.

## Overview

This project pulls historical price data for a configurable watchlist of tickers,
persists it to a time-series table in PostgreSQL, and exposes computed analytics
(daily returns, moving averages, and annualized volatility) via a FastAPI endpoint.
A React frontend consumes the API to render an interactive dashboard with price
charts and a metrics table.

## Stack

**Backend**
- Python
- FastAPI (REST API)
- PostgreSQL (time-series storage)
- pandas (data manipulation & analytics)
- yfinance (market data source)
- psycopg2 (Postgres driver)

**Frontend**
- React + TypeScript
- Vite (build tooling)
- TanStack Query (server state / data fetching)
- Recharts (data visualization)

## What it demonstrates

- Data ingestion from an external market data source
- Time-series data modeling and persistence in PostgreSQL
- Financial analytics: daily returns, rolling moving averages, annualized volatility
- Clean separation of concerns (ingestion, storage, analytics, API as distinct layers)
- REST API design with FastAPI
- Frontend data fetching and visualization

## Architecture

```
ingestion (fetch.py)  ->  PostgreSQL  ->  API (main.py)  ->  React frontend
```

Each layer is independent: analytics functions operate on DataFrames and have no
knowledge of where the data came from; the API composes them.

## Running locally

### Prerequisites
- Python 3.x
- Node.js
- PostgreSQL running locally

### 1. Database setup
```bash
psql postgres
CREATE DATABASE market_dashboard;
\q
```

### 2. Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` (see `.env.example`):

DB_NAME=market_dashboard
DB_USER=your_postgres_user
DB_HOST=localhost
DB_PORT=5432
DB_PASSWORD=

Populate the database with price data:
```bash
cd app
python fetch.py
```

Run the API server:
```bash
uvicorn main:app --reload
```
API available at `http://localhost:8000`. Example: `http://localhost:8000/prices?ticker=TSLA`

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```
Dashboard available at `http://localhost:5173`.

## Configuration

The ticker watchlist is defined in `backend/app/fetch.py`. Database credentials are
managed via environment variables and are not committed to source control.