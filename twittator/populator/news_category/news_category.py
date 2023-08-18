import pandas as pd
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from news_data.models.kaggle_news import KaggleNews

df = pd.read_csv("News_Category_Dataset_v3")