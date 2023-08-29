import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from lang_processing.models.polarity import Polarity
from news_data.models.kaggle_news import KaggleNews
from lang_processing.services.get_polarization import GetPolarization
import json

class PopulatePolarity:
    def populate(self):
        """
        This class/method populates polarization for all of the news that have not gotten a polarization yet.
        It does not receive any params, as all it does is filter the news that have not gotten a polarization
        (has_polarization = False) and runs the polarization calculator with the default params. This will update the attribute 
        has_polarization to False and generate new rows on the polarization table associated with each of the polarized news as 
        a foreign key.
        """
        polarization_calculator = GetPolarization()
        news_data = KaggleNews.objects.filter(
            has_polarization = False
        )
        for news in news_data:
            news_text = f'{news.title} {news.description}'
            
            lemma, mean_polarization, polarity_list, sentic_polarization_list = polarization_calculator.run_with_default_params(news_text)
            
            polarity_object, created = Polarity.objects.get_or_create(
                kagglenews_id = news
            )
            if created:
                polarity_object.relevant_words = json.dumps(lemma, ensure_ascii= False)
                polarity_object.mean_polarization = mean_polarization
                polarity_object.polarization_list = json.dumps(polarity_list)
                polarity_object.sentic_polarization_list = json.dumps(sentic_polarization_list)
                polarity_object.news_pubdate = news.pubdate
                # polarity_object.news_query = news.query_id.query
                news.has_polarization = True
                news.save()
                polarity_object.save()
