import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_ta_indicators import GenerateTechnicalIndicators

df = GenerateTechnicalIndicators('MGLU3.SA', '2020-01-01').run_with_default_params()

print(df)
print(df.columns)