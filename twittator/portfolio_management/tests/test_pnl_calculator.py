import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_ta_indicators import GenerateTechnicalIndicators
from portfolio_management.services.get_stock_pnl import StockPnLCalculator

df = GenerateTechnicalIndicators('MGLU3.SA', '2020-01-01').run_with_default_params()

df = StockPnLCalculator().calculate_pnl(df, 'Close', 5)
print(df)
print(df.columns)