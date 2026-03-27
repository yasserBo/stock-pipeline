import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def get_engine():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url)


def create_table(engine):
    create_sql = """
        CREATE TABLE IF NOT EXISTS stock_prices (
            id          SERIAL PRIMARY KEY,
            date        DATE NOT NULL,
            ticker      VARCHAR(10) NOT NULL,
            open        NUMERIC(10, 4),
            high        NUMERIC(10, 4),
            low         NUMERIC(10, 4),
            close       NUMERIC(10, 4),
            volume      BIGINT,
            daily_return NUMERIC(10, 4),
            ma_7        NUMERIC(10, 4),
            ma_30       NUMERIC(10, 4),
            daily_range NUMERIC(10, 4),
            fetched_at  TIMESTAMP,
            UNIQUE(date, ticker)
        );
    """
    with engine.connect() as conn:
        conn.execute(text(create_sql))
        conn.commit()
    print("Table ready.")


def load_data(df: pd.DataFrame, engine):
    df.to_sql(
        name="stock_prices",
        con=engine,
        if_exists="append",
        index=False,
        method="multi"
    )
    print(f"Loaded {len(df)} rows into stock_prices.")


def verify_load(engine):
    query = """
        SELECT ticker, COUNT(*) as rows, 
               MIN(date) as from_date, 
               MAX(date) as to_date
        FROM stock_prices
        GROUP BY ticker
        ORDER BY ticker;
    """
    with engine.connect() as conn:
        result = pd.read_sql(text(query), conn)
    print("\nData in database:")
    print(result.to_string(index=False))


if __name__ == "__main__":
    engine = get_engine()
    create_table(engine)

    df = pd.read_csv("transformed_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])

    load_data(df, engine)
    verify_load(engine)