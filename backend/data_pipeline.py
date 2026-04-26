import yfinance as yf
import pandas as pd


def load_data(ticker: str, start: str = "2000-01-01", end: str = None, interval: str = "1d"):
    df = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data found for ticker '{ticker}'.")

    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    if isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index()

    if "Datetime" in df.columns and "Date" not in df.columns:
        df = df.rename(columns={"Datetime": "Date"})

    if "Date" not in df.columns:
        raise ValueError("Expected a Date column.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna()
    df = df.drop_duplicates(subset=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    return df


def add_features(df):
    df = df.copy()
    df["Return"] = df["Close"].pct_change()
    df["MA_7"] = df["Close"].rolling(7).mean()
    df["MA_20"] = df["Close"].rolling(20).mean()
    df["Volatility_7"] = df["Return"].rolling(7).std()
    df["High_Low_Range"] = df["High"] - df["Low"]
    df["Target"] = df["Close"].shift(-1)
    df = df.dropna()
    return df


def normalize_data(train_df, val_df, test_df, feature_cols):
    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    for col in feature_cols:
        mean = train_df[col].mean()
        std = train_df[col].std()
        if std == 0:
            std = 1

        train_df[col] = (train_df[col] - mean) / std
        val_df[col] = (val_df[col] - mean) / std
        test_df[col] = (test_df[col] - mean) / std

    return train_df, val_df, test_df

def time_based_split(df, train_size=0.7, val_size=0.15):
    df = df.sort_values("Date").reset_index(drop=True)

    n = len(df)
    train_end = int(n * train_size)
    val_end = int(n * (train_size + val_size))

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    return train_df, val_df, test_df



