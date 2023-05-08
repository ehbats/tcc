from django.db import models

class Query(models.Model):
    id = models.AutoField(primary_key = True)
    query = models.TextField(default="")
    topic = models.TextField(default="")
    before = models.DateField(auto_now_add=True)
    after = models.DateField(auto_now_add=True)
    language = models.TextField(default="")
    country = models.TextField(default="")
    ceid = models.TextField(default="")
    url = models.TextField(default="")
