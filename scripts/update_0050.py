import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone, timedelta

TICKER = "0050.TW"
START = "2014-01-01"

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_PATH = DATA_DIR / "0050_raw.csv"
CLEAN_PATH = DATA_DIR / "0050_clean.csv"

def download_data() -> pd.DataFrame:
    df = yf.download(TICKER, start=START, auto_adjust=False, group_by="column")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Adj Close", "Close", "High", "Low", "Open", "Volume"]]
    df.index.name = "Date"
    return df

def main():
    df = download_data()
    df.to_csv(RAW_PATH)

    clean = df.sort_index().dropna()
    clean.to_csv(CLEAN_PATH)

    tz = timezone(timedelta(hours=8))  # Taiwan time
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"[{now}] Updated {TICKER}")
    print("Rows, Cols:", df.shape)
    print("Range:", df.index.min().date(), "to", df.index.max().date())
    print("Saved:", RAW_PATH, "and", CLEAN_PATH)

if __name__ == "__main__":
    main()
