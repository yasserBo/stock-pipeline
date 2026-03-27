import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.load import get_engine

st.set_page_config(
    page_title="Stock Market Pipeline",
    page_icon="📈",
    layout="wide"
)

@st.cache_resource
def get_db_engine():
    return get_engine()

@st.cache_data
def load_data(ticker):
    engine = get_db_engine()
    query = text("""
        SELECT date, ticker, open, high, low, close,
               volume, daily_return, ma_7, ma_30, daily_range
        FROM stock_prices
        WHERE ticker = :ticker
        ORDER BY date
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"ticker": ticker})
    return df


# ── Sidebar ──────────────────────────────────────────────
st.sidebar.title("Controls")
ticker = st.sidebar.selectbox(
    "Select ticker",
    ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]
)

st.sidebar.markdown("---")
show_ma7  = st.sidebar.checkbox("Show 7-day MA",  value=True)
show_ma30 = st.sidebar.checkbox("Show 30-day MA", value=True)

# ── Load data ─────────────────────────────────────────────
df = load_data(ticker)

# ── Header ────────────────────────────────────────────────
st.title(f"{ticker} — Market Dashboard")
st.caption("Data pipeline: Yahoo Finance → Pandas → PostgreSQL → Streamlit")

# ── Metric cards ──────────────────────────────────────────
latest     = df.iloc[-1]
prev        = df.iloc[-2]
price_delta = round(latest["close"] - prev["close"], 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest close",   f"${latest['close']:.2f}",  f"{price_delta:+.2f}")
col2.metric("Daily return",   f"{latest['daily_return']:.2f}%")
col3.metric("7-day MA",       f"${latest['ma_7']:.2f}")
col4.metric("Daily range",    f"${latest['daily_range']:.2f}")

st.markdown("---")

# ── Candlestick chart ─────────────────────────────────────
st.subheader("Price chart")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df["date"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="OHLC"
))

if show_ma7:
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["ma_7"],
        name="7-day MA",
        line=dict(color="#7F77DD", width=1.5)
    ))

if show_ma30:
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["ma_30"],
        name="30-day MA",
        line=dict(color="#1D9E75", width=1.5)
    ))

fig.update_layout(
    xaxis_rangeslider_visible=False,
    height=450,
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# ── Daily returns chart ───────────────────────────────────
st.subheader("Daily returns (%)")

colors = ["#1D9E75" if r >= 0 else "#D85A30" for r in df["daily_return"]]

fig2 = go.Figure(go.Bar(
    x=df["date"],
    y=df["daily_return"],
    marker_color=colors,
    name="Daily return"
))

fig2.update_layout(
    height=280,
    margin=dict(l=0, r=0, t=10, b=0)
)

st.plotly_chart(fig2, use_container_width=True)

# ── Raw data table ────────────────────────────────────────
with st.expander("View raw data"):
    st.da