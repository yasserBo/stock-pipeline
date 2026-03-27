# Stock Market Data Pipeline

A end-to-end data engineering pipeline that ingests real-time stock market data,
transforms it with Pandas, stores it in PostgreSQL, and visualizes it 
with an interactive Streamlit dashboard.

## Architecture
```
Yahoo Finance API → Ingestion → Transformation → PostgreSQL → Streamlit Dashboard
```

## Features

- Fetches daily OHLCV data for 5 major tickers (AAPL, GOOGL, MSFT, AMZN, META)
- Computes financial indicators: moving averages (7d, 30d), daily returns, volatility
- Stores clean data in a normalized PostgreSQL schema
- Interactive candlestick charts with toggleable moving average overlays
- Modular codebase — each pipeline stage is fully independent

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | Python, yfinance |
| Transformation | Pandas, NumPy |
| Storage | PostgreSQL, SQLAlchemy |
| Orchestration | Modular Python scripts |
| Visualization | Streamlit, Plotly |

## Project Structure
```
stock-pipeline/
├── ingestion/        # Fetches raw data from Yahoo Finance
├── transformation/   # Cleans and enriches raw data
├── storage/          # Loads clean data into PostgreSQL
├── dashboard/        # Streamlit visualization app
├── requirements.txt
└── README.md
```

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/stock-pipeline.git
cd stock-pipeline
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root folder:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_pipeline
DB_USER=postgres
DB_PASSWORD=your_password
```

### 5. Run the pipeline
```bash
python ingestion/fetch.py
python transformation/transform.py
python storage/load.py
```

### 6. Launch the dashboard
```bash
streamlit run dashboard/app.py
```

## What I Learned

- How to design a modular data pipeline with clear separation of concerns
- How to clean and enrich financial data using Pandas
- How to design a PostgreSQL schema and load data with SQLAlchemy
- How to build an interactive data dashboard with Streamlit and Plotly