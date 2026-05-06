import yfinance as yf

df = yf.download("RELIANCE.NS", period="6mo", interval="1d")
print(df.tail())
