import os
import pandas as pd
import yfinance as yf

class FinancialAnalysis:
    def __init__(self):
        directory = './data'
        os.makedirs(directory, exist_ok=True) 
        all_entries = os.listdir(directory)
        file_names = [f for f in all_entries if os.path.isfile(os.path.join(directory, f))]
        close = {}
        self.df_close = {}

        for i in file_names:
            symbol_str = i.split("_")[0]
            self.update_stock(symbol_str)  # updates CSV first
            df = pd.read_csv(f"data/{symbol_str}_daily.csv", index_col=0)  # read the updated CSV
            close[symbol_str] = df['close']
        self.df_close = pd.DataFrame(close).sort_index().fillna(method="ffill")

    def fetch_stock(self, symbol):
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{symbol}_daily.csv"

        if os.path.exists(file_path):
            return self.update_stock(symbol)
        
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="max")
            if df.empty or df['Open'].sum() == 0:
                print(f"{symbol} does not exist or has no data")
                return
        except Exception as e:
            print(f"Failed to fetch {symbol}: {e}")
            return None
        
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
    
    def update_stock(self, symbol):
        file_path = f"data/{symbol}_daily.csv"
        today = pd.Timestamp.today().normalize()

        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            last_date = df.index.max()
            start_date = last_date + pd.Timedelta(days=1)

            if start_date > today:
                print(f"{symbol} already up to date ✅")
                return df

            ticker = yf.Ticker(symbol)
            new_data = ticker.history(start=start_date, end=today)
            if new_data.empty:
                print(f"No new data for {symbol} ❌")
                return df

            new_data.index = new_data.index.tz_localize(None)
            new_data = new_data.drop(columns=["Dividends", "Stock Splits"])
            new_data = new_data.rename(columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            })
            new_data = new_data.round({"open": 2, "high": 2, "low": 2, "close": 2})

            # append new rows to old df
            updated = pd.concat([df, new_data])
            updated = updated[~updated.index.duplicated(keep="last")]  # remove duplicates
            updated.to_csv(file_path)

            print(f"{symbol} updated to {today.date()} ✅")
            return updated

        else:
            print("Something went wrong")
            return
    
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