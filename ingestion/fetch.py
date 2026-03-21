import yfinance as yf
import pandas as pd
from datetime import datetime

TICKERS = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]

def fetch_stock_data(tickers: list, period: str = "3mo") -> pd.DataFrame:
    all_data = []

    for ticker in tickers:
        print(f"Fetching {ticker}...")
        raw = yf.download(ticker, period=period, auto_adjust=True)

        raw = raw.reset_index()
        raw.columns = [col[0] if isinstance(col, tuple) else col for col in raw.columns]
        raw["ticker"] = ticker
        raw["fetched_at"] = datetime.now()

        all_data.append(raw)

    df = pd.concat(all_data, ignore_index=True)

    df.columns = [c.lower() for c in df.columns]

    print(f"\nFetched {len(df)} rows for {len(tickers)} tickers.")
    return df


if __name__ == "__main__":
    df = fetch_stock_data(TICKERS)
    print(df.head(10))
    df.to_csv("raw_data.csv", index=False)
    print("Saved to raw_data.csv")