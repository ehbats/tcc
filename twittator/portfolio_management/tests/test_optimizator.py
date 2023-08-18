import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_price_data import GetPriceData
from portfolio_management.services.base_optimizator import Optimizator
import numpy as np

dictionary = {
    'PETR4': {
        'weight': 0.6,
        'return': 1
    },
    'MGLU3': {
        'weight': 0.1, 
        'return': -1
    },
    'ITUB4': {
        'weight': 0.3,
        'return': 3
    }
}
Optimizator.get_portfolio_return_from_dict(dictionary)


df_list = [GetPriceData().get_price_data('PETR4.SA', '2023-01-01'), GetPriceData().get_price_data('MGLU3.SA', '2023-01-01'), GetPriceData().get_price_data('ITUB4.SA', '2023-01-01')]
merged_dfs = Optimizator.merge_dataframes(df_list, ['Close', 'Open'], ['PETR4', 'MGLU3', 'ITUB4'])

matrix = Optimizator.get_portfolio_covariance_matrix(merged_dfs, ['Open PETR4', 'Open MGLU3', 'Open ITUB4'])

variance = Optimizator.get_portfolio_variance(np.array([[0.6, 0.1, 0.3]]), matrix)
