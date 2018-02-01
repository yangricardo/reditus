from django.db import models
from django_pandas.managers import DataFrameManager
# Create your models here.

class Processo(models.Model):
    processo = models.TextField()
    sentenca = models.TextField()
    similar_file = models.TextField()
    similar_processo = models.TextField()

    objects = models.Manager()
    pobjects = DataFrameManager()