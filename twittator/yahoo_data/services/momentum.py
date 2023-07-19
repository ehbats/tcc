import pandas as pd

class GetMomentumIndicators():
    def get_roc(self, df: pd.DataFrame, window: int = 14):
        df['roc'] = (df['Close'] - df['Close'].shift(window)) / df['Close'].shift(window)

        return df
    
    def get_roc_percentage(self, df: pd.DataFrame, window: int = 10):
        df['roc_perc'] = (df['Close'] - df['Close'].shift(window)) * 100 / df['Close'].shift(window)

        return df
    
    def get_momentum(self, df: pd.DataFrame, window: int = 10):
        df['momentum'] = df['Close'] * 100 / df['Close'].shift(window)

        return df

    def get_chande(self, df: pd.DataFrame, window: int = 14):
        df['chande'] = (df['High'].rolling(window).sum() * df['Low'].rolling(window).sum()) \
        /                                                                             \
        (df['High'].rolling(window).sum() +  df['Low'].rolling(window).sum())         \

        return df
    
    def get_ewma(self, df: pd.DataFrame, span: int = 12, column: str = 'Close'):
        df[f'EWMA{span}'] = df[column].ewm(span=span).mean()

        return df
    
    def run_with_standard_intervals(self, df: pd.DataFrame):
        df = self.get_chande(df = df)
        df = self.get_momentum(df = df)
        df = self.get_roc_percentage(df = df)
        df = self.get_roc(df = df)
        df = self.get_ewma(df = df)
        
        return df