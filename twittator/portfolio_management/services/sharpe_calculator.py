import pandas as pd

class SharpeCalculator:
    def calculate(self, benchmark_data: pd.DataFrame, portfolio_data: pd.DataFrame, capitalization_column: str = 'capitalization'):
        portfolio_return = self.__calculate_return_pct(portfolio_data[capitalization_column])
        benchmark_return = self.__calculate_return_pct(benchmark_data[capitalization_column])
        portfolio_std = self.__calculate_std(portfolio_data[capitalization_column])
        
        self.sharpe_ratio = (portfolio_return - benchmark_return) / portfolio_std

        return self.sharpe_ratio

    def __calculate_std(self, capitalization_series: pd.Series):
        return capitalization_series.std()

    def __calculate_return_pct(self, capitalization_series: pd.Series):
        return (capitalization_series.iloc[-1]/capitalization_series.iloc[0]) - 1