import os
import requests
import pandas as pd
from dotenv import load_dotenv
import seaborn as sns
import matplotlib.pyplot as plt

# load_dotenv()
# api_key = os.getenv("ALPHA_VANTAGE_KEY")

# url = "https://www.alphavantage.co/query"
# params = {
#     "function": "TIME_SERIES_DAILY",
#     "symbol": "TSLA",
#     "apikey": api_key
# }

class FinancialAnalysis:
    def __init__(self):
        # Load all CSVs and keep only the closing prices
        aapl = pd.read_csv("data/AAPL_daily.csv", index_col=0)
        msft = pd.read_csv("data/MSFT_daily.csv", index_col=0)
        amzn = pd.read_csv("data/AMZN_daily.csv", index_col=0)
        blk = pd.read_csv("data/BLK_daily.csv", index_col=0)
        tsla = pd.read_csv("data/TSLA_daily.csv", index_col=0)
        
        # Combine into one table
        self.df_close = pd.DataFrame({
            "AAPL": aapl["close"],
            "MSFT": msft["close"],
            "AMZN": amzn["close"],
            "BLK": blk["close"],
            "TSLA": tsla["close"]
        })

        # Convert dates and sort
        self.df_close.index = pd.to_datetime(self.df_close.index)
        self.df_close = self.df_close.sort_index()

    def daily_changes(self):
        # How much each number changed from the day before
        return self.df_close.pct_change()

    def correlation_matrix(self):
        # How columns move relative to each other
        returns = self.daily_changes()
        return returns.corr()

    def volatility(self, window=10):
        # How jumpy the numbers are over time
        returns = self.daily_changes()
        return returns.rolling(window).std()


# Usage
app = FinancialAnalysis()

print("Stock Prices:")
print(app.df_close)

print("\nDaily Changes:")
print(app.daily_changes())

print("\nCorrelation Matrix:")
print(app.correlation_matrix())

print("\nVolatility (10-day window):")
print(app.volatility().iloc[-10:-1])
