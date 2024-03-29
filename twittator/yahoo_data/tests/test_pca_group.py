import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_ta_indicators import GenerateTechnicalIndicators
from yahoo_data.services.get_pca import GeneratePCAByGrouping

df = GenerateTechnicalIndicators(
    'MGLU3.SA', 
    '2020-01-01'
).run_with_default_params()

groups = [
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

group = GeneratePCAByGrouping().generate_pca(df = df, groupings = groups)

print(group)