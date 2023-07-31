import pandas as pd
from datetime import date
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from portfolio_management.services.markowitz_optimizator import MarkowitzOptimizator

class BenchmarkComparator(MarkowitzOptimizator):
    def get_benchmark_data(self, start_date: date, end_date: date, benchmark: str, initial_investment: float = 1):
        if benchmark == 'CDI' or benchmark == 'SELIC':
            return self.get_selic_benchmark(start_date, end_date, initial_investment)
        
    def get_selic_benchmark(self, start_date: date, end_date: date, initial_investment: float = 1):
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
            