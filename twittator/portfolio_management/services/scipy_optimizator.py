from base_optimizator import Optimizator

class SciPyOptimizator(Optimizator):
    def optimize(self, dfs):
        covariance = self.get_portfolio_covariance_matrix()