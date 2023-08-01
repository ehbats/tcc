import pandas as pd
from datetime import date
import sys, os
import yfinance as yf
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from portfolio_management.services.markowitz_optimizator import MarkowitzOptimizator
from yahoo_data.services.get_price_data import GetPriceData
from portfolio_management.services.get_stock_pnl import StockPnLCalculator

class BenchmarkComparator(MarkowitzOptimizator):
    def get_benchmark_data(self, start_date: date, end_date: date, benchmark: str, initial_investment: float = 1, ibov_column: str = 'Close'):
        if benchmark == 'CDI' or benchmark == 'SELIC':
            return self.get_selic_benchmark(start_date, end_date, initial_investment)
        if benchmark == 'IBOV' or benchmark == 'IBOVESPA':
            return self.get_ibov_benchmark(start_date, end_date, initial_investment, ibov_column)
        
    def get_selic_benchmark(self, start_date: date, end_date: date, initial_investment: float):
        parsed_start = start_date.strftime('%d/%m/%Y')
        parsed_end = end_date.strftime('%d/%m/%Y')

        link = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial={parsed_start}&dataFinal={parsed_end}"

        selic_dataframe = pd.read_json(link)

        selic_dataframe['capitalization'] = selic_dataframe.apply(
            self.get_return_from_initial_investment,
            axis=1,
            initial_investment=initial_investment,
            column='valor',
            is_percentage=True,
        )

        return selic_dataframe
    
    def get_ibov_benchmark(self, start_date: date, end_date: date, initial_investment: float, ibov_column: str):
        ibov = GetPriceData().get_price_data('^BVSP', start_date, end_date)
        
        ibov_returns = StockPnLCalculator().calculate_pnl(
            ibov,
            ibov_column,
            fillna=True
        )
        
        ibov['capitalization'] = ibov_returns.apply(
            self.get_return_from_initial_investment,
            axis=1,
            initial_investment=initial_investment,
            column=f'{ibov_column} PnL {1} days'
        )
        ibov.reset_index(inplace=True)
        ibov['Date'] = ibov['Date'].dt.strftime('%d/%m/%Y')
        return ibov
