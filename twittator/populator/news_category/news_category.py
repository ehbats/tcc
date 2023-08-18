import pandas as pd
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from news_data.models.kaggle_news import KaggleNews

df = pd.read_json("./populator/news_category/News_Category_Dataset_v3.json", lines=True)

print(df)