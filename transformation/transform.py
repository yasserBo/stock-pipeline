import pandas as pd
import numpy as np

def transform_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    print("Starting transformation...")

    # 1. Drop rows with missing prices
    df = df.dropna(subset=["open", "high", "low", "close", "volume"])
    
    # 2. Ensure correct data types
    df["date"] = pd.to_datetime(df["date"])
    df["volume"] = df["volume"].astype(int)

    # 3. Sort by ticker and date
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

    # 4. Daily return — how much % the stock moved each day
    df["daily_return"] = df.groupby("ticker")["close"].pct_change() * 100

    # 5. 7-day moving average
    df["ma_7"] = (
        df.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(window=7).mean())
    )

    # 6. 30-day moving average
    df["ma_30"] = (
        df.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(window=30).mean())
    )

    # 7. Daily price range (high - low)
    df["daily_range"] = df["high"] - df["low"]

    # 8. Round all float columns to 4 decimal places
    float_cols = df.select_dtypes(include=[np.floating]).columns
    df[float_cols] = df[float_cols].round(4)

    print(f"Transformation complete. {len(df)} rows ready.")
    return df


if __name__ == "__main__":
    raw = pd.read_csv("raw_data.csv")
    cleaned = transform_stock_data(raw)
    print(cleaned[["date", "ticker", "close", "daily_return", "ma_7", "ma_30"]].head(15))
    cleaned.to_csv("transformed_data.csv", index=False)
    print("Saved to transformed_data.csv")