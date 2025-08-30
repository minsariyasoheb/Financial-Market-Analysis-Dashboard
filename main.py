import os
import pandas as pd
import yfinance as yf

class FinancialAnalysis:
    def __init__(self):
        directory = './data'
        os.makedirs(directory, exist_ok=True) 
        all_entries = os.listdir(directory)
        file_names = [f for f in all_entries if os.path.isfile(os.path.join(directory, f))]
        symbols = []
        close = {}
        self.df_close = {}

        for i in file_names:
            symbols.append(i.split("_")[0])
            symbol = pd.read_csv(f"data/{i.split("_")[0]}_daily.csv", index_col=0)
            close[i.split("_")[0]] = symbol['close']
        self.df_close = pd.DataFrame(close).sort_index().fillna(method="ffill")

    def fetch_stock(self, symbol):
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{symbol}_daily.csv"

        if os.path.exists(file_path):
            print(f"{symbol} already exists, skipping ✅")
            return pd.read_csv(file_path, index_col=0)
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="max")
        df.index = df.index.tz_localize(None)
        df = df.drop(columns=["Dividends", "Stock Splits"])
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })
        df = df.round({"open": 2, "high": 2, "low": 2, "close": 2})
        df = df.reset_index()
        df.to_csv(f"data/{symbol}_daily.csv", index=False)
        print(f"Saved {symbol} full history ✅")
        symbol_data = pd.read_csv(f"data/{symbol}_daily.csv", index_col=0)
        self.df_close[symbol] = symbol_data['close']
        return df
    
    def daily_changes(self):
        # How much each number changed from the day before
        return self.df_close.pct_change()

    def correlation_matrix(self):
        # How columns move relative to each other
        returns = self.daily_changes()
        return returns.corr()

    def volatility(self, window=10):
        returns = self.daily_changes()
        vol = returns.rolling(window).std() * 100   # convert to %
        print(f"\nVolatility ({window}-day window) [%]:")
        return vol.tail(window)   # show last 'window' rows

# Usage
app = FinancialAnalysis()

print("Stock Prices:")
print(app.df_close)

print("\nDaily Changes:")
print(app.daily_changes())

print("\nCorrelation Matrix:")
print(app.correlation_matrix())

print(app.volatility())