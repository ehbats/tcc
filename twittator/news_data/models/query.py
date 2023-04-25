from django.db import models

class Query(models.Model):
    id = models.AutoField(primary_key = True)
    query = models.TextField()
    topic = models.TextField()
    before = models.DateField()
    after = models.DateField()
    language = models.TextField()
    country = models.TextField()
    ceid = models.TextField()
    url = models.TextField()