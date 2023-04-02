from poc_calculate_indicators import GenerateTechnicalIndicators

df = GenerateTechnicalIndicators('MGLU3.SA', '2020-01-01').run_with_default_params()

print(df)
print(df.columns)