import pandas as pd
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from news_data.models.kaggle_news import KaggleNews

def populate_kaggle_news(row: pd.Series):
    news_obj, created = KaggleNews.objects.get_or_create(
        title=row['title'],
        country='BRZ'
    )

    if created:
        category = 'BUSINESS' if row['category'] == 'mercado' else row['category']
        news_obj.description = row['text']
        news_obj.has_description = True
        news_obj.source = 'Folha de Sao Paulo'
        news_obj.pubdate = row['date']
        news_obj.category = category
        news_obj.kaggle_url = 'https://www.kaggle.com/datasets/marlesson/news-of-the-site-folhauol?resource=download'
        news_obj.kaggle_name = 'News of the Brazilian Newspaper'
        news_obj.save()

df = pd.read_csv('./populator/news_of_the_brazilian_newspaper/articles.csv')

df.apply(populate_kaggle_news, axis=1)