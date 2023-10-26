import pandas as pd
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from news_data.models.kaggle_news import KaggleNews

df = pd.read_csv('./populator/noticias_publicadas_no_brasil/Historico_de_materias.csv')

def populate_kaggle_news(row: pd.Series):
    news_obj, created = KaggleNews.objects.get_or_create(
        title=row['titulo'],
        country='BRZ'
    )

    if created:
        category = 'BUSINESS' if row['assunto'] == 'economia' else row['assunto']
        news_obj.description = row['conteudo_noticia']
        news_obj.has_description = True
        news_obj.source = 'O Globo'
        news_obj.pubdate = row['data']
        news_obj.category = category
        news_obj.kaggle_url = 'https://www.kaggle.com/datasets/diogocaliman/notcias-publicadas-no-brasil'
        news_obj.kaggle_name = 'Noticias publicadas no Brasil'
        news_obj.save()

df = df.dropna()
df.apply(populate_kaggle_news, axis=1)