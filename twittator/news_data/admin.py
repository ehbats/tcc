from django.contrib import admin
from news_data.models.news import News
from news_data.models.query import Query

admin.site.register(News)
admin.site.register(Query)
