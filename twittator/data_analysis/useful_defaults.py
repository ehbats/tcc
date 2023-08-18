GROUPS = [
        {
            "group_name": 'trend_pca',
            "group_columns": ['sma', 'wma', 'cci']
        },
        {
            "group_name": "mean_reversion_pca",
            "group_columns": ['fast_stoch', 'fast_signal', 'slow_stoch', 'slow_signal']
        },
        {
            "group_name": "relative_strength_pca",
            "group_columns": ['rsi', 'williams_r']
        },
        {
            "group_name": "volume_pca",
            "group_columns": ["on_balance", "MFI"]
        },
        {
            "group_name": "momentum_pca",
            "group_columns": ["macd", "roc", "roc_perc", "momentum" , "chande"]
        }
]

IBOVESPA = {
    'bench': 'INDEX',
    'bench_name': 'IBOVESPA',
    'column': 'Close',
    'date_column': 'Date',
    'ticker': '^BVSP'
}
SP500 = {
    'bench': 'INDEX',
    'bench_name': 'S&P500',
    'column': 'Close',
    'date_column': 'Date',
    'ticker': '^GSPC'
}

CDI = {
    'bench': 'CDI',
    'bench_name': 'CDI',
    'column': 'valor',
    'date_column': 'data'
}