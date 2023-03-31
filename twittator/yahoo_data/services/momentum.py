import pandas as pd

class GetMomentumIndicators():
    def get_roc(df: pd.DataFrame, window: int = 10):
        roc = (df['Close'] - df['Close'].shift(window)) / df['Close'].shift(window)

        return roc
    
    def get_roc_percentage(df: pd.DataFrame, window: int = 14):
        roc = (df['Close'] - df['Close'].shift(window)) * 100 / df['Close'].shift(window)

        return roc
    
    def get_momentum(df: pd.DataFrame, window: int = 10):
        momentum = df['Close'] * 100 / df['Close'].shift(window)

        return momentum

    def get_chande(df: pd.DataFrame, window: int = 14):
        chande = (df['High'].rolling(window).sum() * df['Low'].rolling(window).sum()) \
        /                                                                             \
        (df['High'].rolling(window).sum() +  df['Low'].rolling(window).sum())         \

        return chande