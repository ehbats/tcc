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
        title=row['headline'],
        country='USA',
    )
    if created:
        news_obj.description = row['short_description']
        news_obj.has_description = True
        news_obj.source = 'HuffPost'
        news_obj.pubdate = row['date']
        news_obj.category = row['category']
        news_obj.kaggle_url = 'https://www.kaggle.com/datasets/rmisra/news-category-dataset'
        news_obj.kaggle_name = 'News Category Dataset'
        news_obj.save()

df = pd.read_json("./populator/news_category/News_Category_Dataset_v3.json", lines=True)

df.apply(populate_kaggle_news, axis=1)