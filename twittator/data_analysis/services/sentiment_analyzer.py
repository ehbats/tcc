from datetime import date, datetime, timedelta
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from lang_processing.services.generate_polarization_df import GeneratePolarizationDataFrame

class CountSentimentAnalyzer:
    def __init__(self):
        self.vneg_ratio_list = []
        self.neg_ratio_list = []
        self.neutral_ratio_list = []
        self.pos_ratio_list = []
        self.vpos_ratio_list = []

    def analyze(self, start_date: date | str, query: dict = {}, periods: int = 5):
        result_ratios = self.generate_ratios(start_date, query, periods)
        self.vneg_ratio_list.append(result_ratios['very_positive_ratio'])
        self.neg_ratio_list.append(result_ratios['positive_ratio'])
        self.neutral_ratio_list.append(result_ratios['neutral_ratio'])
        self.pos_ratio_list.append(result_ratios['negative_ratio'])
        self.vpos_ratio_list.append(result_ratios['very_negative_ratio'])

    def generate_ratios(self, date: date | str, query: dict, periods: int):
        polarization_list, sentic_polarization_list, date_polarity, date_sentics = GeneratePolarizationDataFrame().get_news_n_days_prior(date=date, query=query, periods=periods)
        
        very_negative_list = []
        negative_list = []
        neutral_list = []
        positive_list = []
        very_positive_list = []
        for score in polarization_list:
            if score > 0.75:
                very_positive_list.append(score)
            elif score > 0.25:
                positive_list.append(score)
            elif score > -0.25:
                neutral_list.append(score)
            elif score > -0.75:
                negative_list.append(score)
            else:
                very_negative_list.append(score)
        if len(polarization_list) == 0:
            return {'very_positive_ratio': 0,
                'positive_ratio': 0,
                'neutral_ratio': 0,
                'negative_ratio': 0,
                'very_negative_ratio': 0}

        return {'very_positive_ratio': len(very_positive_list) / len(polarization_list),
                'positive_ratio': len(positive_list) / len(polarization_list),
                'neutral_ratio': len(neutral_list) / len(polarization_list),
                'negative_ratio': len(negative_list) / len(polarization_list),
                'very_negative_ratio': len(very_negative_list) / len(polarization_list)}

class CountAndAgreementAnalyzer:
    def __init__(self, base_query: dict):
        self.polarization_generator = GeneratePolarizationDataFrame(base_query)
        self.positive_count_list = []
        self.agreement_list = []
        self.positive_ratio_list = []

    def analyze(self, start_date: date | str, query: dict = {}, periods: int = 5, positivity_ratio: float = 0.5):
        result_ratios = self.generate_ratios(start_date, query, periods, positivity_ratio)
        self.positive_count_list.append(result_ratios['positive_count'])
        self.agreement_list.append(result_ratios['agreement_ratio'])
        self.positive_ratio_list.append(result_ratios['positive_ratio'])

    def generate_ratios(self, start_date: date | str, query: dict, periods: int, positivity_ratio: float):
        _foo, _bar, _lorem, date_total_news_sentics = self.polarization_generator.get_news_n_days_prior_from_base_query(start_date, query, periods)

        positive_count = 0

        for specific_news_sentic_list in date_total_news_sentics:
            total_polarizations = len(specific_news_sentic_list)
            total_positive = len([sentic for sentic in specific_news_sentic_list if sentic > 0])
            
            if total_positive/total_polarizations > positivity_ratio:
                positive_count += 1
        
        total_count = len(date_total_news_sentics)
        if total_count > 0:
            positive_ratio = positive_count / len(date_total_news_sentics)
            negative_count = total_count - positive_count

            agreement_ratio = (positive_count - negative_count) / total_count
        else:
            positive_ratio = 0
            agreement_ratio = 0

        return {
            'positive_count': positive_count,
            'positive_ratio': positive_ratio,
            'agreement_ratio': agreement_ratio
        }
