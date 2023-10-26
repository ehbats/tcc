from django.contrib import admin
from news_data.models.news import News
from news_data.models.query import Query
from news_data.models.kaggle_news import KaggleNews

admin.site.register(News)
admin.site.register(Query)
admin.site.register(KaggleNews)