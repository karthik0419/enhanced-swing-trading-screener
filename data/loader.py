import yfinance as yf
import pandas as pd


def _clean_df(df):
    """Standardize dataframe (very important for stability)"""

    if df is None or df.empty:
        return None

    # ✅ Proper multi-index handling
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Keep only required columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    df.dropna(inplace=True)

    return df


# -----------------------
# SINGLE TIMEFRAME
# -----------------------
def fetch_data(symbol, period="6mo", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval)
    return _clean_df(df)


# -----------------------
# MULTI TIMEFRAME
# -----------------------
def fetch_multi_tf(symbol):
    try:
        df_daily = yf.download(symbol, period="6mo", interval="1d")
        df_weekly = yf.download(symbol, period="2y", interval="1wk")
        df_4h = yf.download(symbol, period="3mo", interval="1h")  # proxy for 4H

        df_daily = _clean_df(df_daily)
        df_weekly = _clean_df(df_weekly)
        df_4h = _clean_df(df_4h)

        return df_daily, df_weekly, df_4h

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None, None, None