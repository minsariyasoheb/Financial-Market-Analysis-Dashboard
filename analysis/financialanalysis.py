import os
import pandas as pd
import yfinance as yf
import streamlit as st
from analysis.visualization import visualizations

class FinancialAnalysis:
    def __init__(self):
        self.viz = visualizations()
        directory = './data'
        os.makedirs(directory, exist_ok=True) 
        all_entries = os.listdir(directory)
        file_names = [f for f in all_entries if os.path.isfile(os.path.join(directory, f))]
        close = {}
        self.df_close = {}

        for i in file_names:
            symbol_str = i.split("_")[0]
            df = self.update_stock(symbol_str)
            close[symbol_str] = df['close']
        self.df_close = pd.DataFrame(close).sort_index().ffill()

    def fetch_stock(self, symbol):
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{symbol}_daily.csv"

        if os.path.exists(file_path):
            return self.update_stock(symbol)
        
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1y")
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
        print(f"Saved {symbol} full history ")
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
                print(f"{symbol} already up to date ")
                return df

            ticker = yf.Ticker(symbol)
            new_data = ticker.history(start=start_date, end=today)
            if new_data.empty:
                print(f"No new data for {symbol} ")
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

            print(f"{symbol} updated to {today.date()} ")
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
        return vol.tail(window)   # show last 'window' rows
        
    def plot_prices(self, symbols=None, days=100):
        if symbols is None:
            symbols = self.df_close.columns[:5]  # first 5 by default
        data_to_plot = self.df_close[symbols].tail(days)
        st.line_chart(data_to_plot)
    
    def plot_daily_changes(self, symbols=None, days=100, bins=50):
        # Compute daily changes
        changes = self.daily_changes().tail(days)

        # Select symbols or default to first 5
        if symbols is None:
            symbols = changes.columns[:5]
        changes = changes[symbols].dropna()

        # Plot histogram
        for col in changes.columns:
            self.viz.line_chart(
                changes[col],
                title=f"Daily Changes: {col}",
                x_axis="Change [%]",
                y_axis="Frequency"
            )

    def plot_correlation_matrix(self, symbols=None, days=100):
        # Compute daily changes and limit to last 'days'
        changes = self.daily_changes().tail(days)

        # Select symbols or default to first 5
        if symbols is None:
            symbols = changes.columns[:5]
        changes = changes[symbols].dropna()

        # Compute correlation matrix
        corr = changes.corr()

        # Plot heatmap
        self.viz.heatmap(corr, title="Correlation Matrix")

    def plot_volatility(self, symbols=None, window=10, days=100):
        # Compute volatility
        vol = self.volatility(window=window).tail(days)

        # Select symbols or default to first 5
        if symbols is None:
            symbols = vol.columns[:5]
        vol = vol[symbols].dropna()

        # Plot each symbol
        for col in vol.columns:
            self.viz.line_chart(
                vol[col],
                title=f"{window}-day Volatility: {col}",
                x_axis="Date",
                y_axis="Volatility [%]"
            )