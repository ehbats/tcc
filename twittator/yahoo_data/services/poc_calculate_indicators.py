from poc_get_data import get_price_data

tickers = ['MGLU3.SA', 'PETR4.SA', 'ITUB4.SA']
start_date = '2022-01-01'
end_date = '2023-01-05'

results = get_price_data(
    tickers = tickers,
    start_date = start_date,
    end_date = end_date
    )

print(results)