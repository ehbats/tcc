import pandas as pd
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from news_data.models.kaggle_news import KaggleNews
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
from datetime import datetime

o_globo_filters = ['Economia', 'Panorama Econômico', 'Caderno Economia',' Empresas', 'Eonomia', 'Econoia', 'Economoa', 'Evonomia', 'Finanças', 'Econoimia', 'Econommia', 'Coluna Panorama Econômico', 'Ecconomia', 'Economico']
valor_economico_filters = ['Finanças', 'Empresas', 'Rumos Da Economia', 'Empresa',' Investimentos', 'Lucro E Competitividade', 'Finança', 'Empresas E Serviços', 'Economia', 'Finanfas', 'Caderno Empresas', 'Dinheiro', 'Financas', 'Empresas Tendências E Consumo', 'Emnpresas', 'Eu E Investimentos', 'Imvestimentos', 'Caderno Finanças', 'Emrpesas', 'Especial Fundos De Investimentos', 'Epresas', 'Finaças', 'Caderno Empresas Indústria', 'Finanças D', 'Empresas E Tecnologia', 'Mercado', 'Finanaças', 'Empresa E Indústria', 'Emrpresas', 'Esmpresas', 'Empreasa', 'Financças', 'Fianças', 'Finanaçs', 'Financeira', 'Finacas', 'Juros', 'Financeiro', 'Crédito Para Empresa', 'Hora De Investir', 'Investimetos', 'Investimeto', 'Empreas', 'Crédito', 'Mercado Financeiro', 'Empesas', 'Comércio', 'Finanças E Mercados', 'Valor Finanças', 'Empresas E Tendências E Consumo', 'Mercado Altera Expectativas Para Rumo Da Selic Em', 'Fiinanças']
total_list = o_globo_filters + valor_economico_filters
def populate_kaggle_news(row: pd.Series):
    if len(row['title']) > 2500:
        row['title'] = row['title'][:2500]
    parsed_date = True
    
    try:
        pubdate = datetime.strptime(row['date'], '%d/%m/%Y')
    except:
        parsed_date = False

    if row['citation'] == None:
        parsed_date = False
    
    if parsed_date:
        news_obj, created = KaggleNews.objects.get_or_create(
            title=row['title'],
            country='BRZ'
        )

        if created:
            source, category = row['citation'].split(' : ')
            category = 'BUSINESS' if category in total_list else category
            news_obj.description = row['html']
            news_obj.has_description = True
            news_obj.source = source
            news_obj.pubdate = pubdate
            news_obj.category = category
            news_obj.kaggle_url = 'https://www.kaggle.com/datasets/fogelman/brazilian-news'
            news_obj.kaggle_name = 'Brazilian news'
            news_obj.save()

def parse_citation(row: pd.Series):
    citation = row['citation'].title()
    if 'O Globo' in citation:
        text_pattern = re.compile(r'^([a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ] ?)+$')
        text_list = []
        for text in citation.split(', '):
            if text_pattern.match(text.strip()):
                text_list.append(text.strip())
        if len(text_list) > 1:
            text = f"O Globo : {text_list[1]}"
            return text
        return 'O Globo : MISSING_CATEGORY'
    if 'Valor Econ' in citation:
        text_pattern = re.compile(r'^([a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ] ?)+$')
        text_list = []
        for text in citation.split(', '):
            if text_pattern.match(text.strip()):
                text_list.append(text.strip())
        if len(text_list) > 1:
            text = f"Valor Economico : {text_list[1]}"
            return text
        return 'Valor Economico : MISSING_CATEGORY'
    return None

def tag_visible(element):
    """
    Gets all of the elements that are visible to the user.
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def parse_html(row: pd.Series):
    html = row['html']
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(string = True)
    filtered_html = filter(tag_visible, texts)  
    parsed_texts = u" ".join(t.strip() for t in filtered_html)

    return parsed_texts

df = pd.read_csv('./populator/brazilian_news/news.csv')
df = df.dropna()
# print(df.loc[df['date'] == '07/2018'])
df['citation'] = df.apply(parse_citation, axis=1)
df['html'] = df.apply(parse_html, axis=1)
df = df.dropna()
df.apply(populate_kaggle_news, axis=1)