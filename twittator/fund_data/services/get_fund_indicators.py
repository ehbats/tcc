import pandas as pd

class GetFundIndicators:
    def get_relevant_share_price_rationality(
            self,
            df: pd.DataFrame
            ):
        """
        Receives a pandas DataFrame containing the company's
        fundamental data and generates the indicators:
        - Book value per share: (total equity - preferred equity) / total shares outstanding
        - Cash flow per share: (cash flow - preferred dividends) / shares outstanding
        - Retention ratio = (net income - dividends) / net income
        """
        pass

    def get_profitability(
            self,
            df: pd.DataFrame
            ):
        """
        Receives a pandas DataFrame containing the company's
        fundamental data and generates the indicators:
        - Return on equity (after tax): net income after tax / shareholder's equity
        - Earnings per share: (net income preferred dividends) / shares outstanding
        - Net profit margin: net income after tax / net sales
        - Gross profit margin: gross profit / net sales
        - Net profits = total revenue - total expenses
        - Operating earnings per share: operating income / shares outstanding
        TODO: evaluate the 23 indicator on the article
        """
        pass

    def get_efficiency(
            self,
            df: pd.DataFrame
            ):
        """
        Receives a pandas DataFrame containing the company's
        fundamental data and generates the indicators:
        - Receivable turnover ratio: net credit sales / average accounts receivable
        - Current assets turnover ratio: sales revenue / average current assets
        TODO: evaluate indicators 26 and 28
        """
        pass

    def get_growth(
            self,
            df: pd.DataFrame
            ):
        """
        Receives a pandas DataFrame containing the company's
        fundamental data and generates the indicators:
        - Operating revenue growth (%): (operating revenue(t) - operating revenue(t-1)) / operating revenue(t)
        - Net profit growth (%): (net profit(t) - net profit(t-1)) / net profit(t)
        - Net assets growth(%): (net assets(t) - net assets(t-1)) / net assets(t)
        - Total assets growth (%): (total assets(t) - total assets(t-1)) / total assets(t)
        - Earnings per share growth (%): (earnings per share(t) - earnings per share(t-1)) / earnings per share(t)
        """
        pass

    def get_leverage(
            self,
            df: pd.DataFrame
            ):
        """
        Receives a pandas DataFrame containing the company's
        fundamental data and generates the indicators:
        - Current ratio: current assets / current liabilities
        - Quick ratio: quick assets / current liabilities
        - Cash ratio: (cash + marketable securities) / current liabilities
        - Shareholder equity ratio: total shareholder equity / total assets
        """
        pass

    def get_liquidity(
            self,
            df: pd.DataFrame
            ):
        """
        Receives a pandas DataFrame containing the company's
        fundamental data and generates the indicators:
        - Operating cash flow to net sales ratio: operating cash flow / net sales
        - Operating cash flow to total assets ratio: operating cash flow / total assets
        - Operating cash flow to net revenue ratio: operating cash flow / net revenue
        - Operating cash flow to net income ratio: operating cash flow / net income
        - EBITDA to interest expense ratio: EBITDA / interest expense
        """
        pass
    def get_indicators(
            self,
            df: pd.DataFrame
            ):
        """
        Receives a pandas DataFrame and runs all methods of this class incorporating all of the fundamental analysis
        indicators at once.
        """
        df = self.get_relevant_share_price_rationality(df)
        df = self.get_profitability(df)
        df = self.get_efficiency(df)
        df = self.get_growth(df)
        df = self.get_leverage(df)
        df = self.get_liquidity(df)

        return df