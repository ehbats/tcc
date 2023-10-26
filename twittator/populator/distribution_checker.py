import pandas as pd
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from news_data.models.kaggle_news import KaggleNews
import matplotlib.pyplot as plt
qs = KaggleNews.objects.filter(
    pubdate__gte = '2015-01-01',
    pubdate__lte = '2018-01-01',
    category = 'BUSINESS'
).order_by('pubdate')
df = pd.DataFrame(list(qs.values('pubdate')))
plt.hist(df['pubdate'])
plt.show()