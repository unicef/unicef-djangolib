from django.db import models


class DemoModel(models.Model):
    name = models.CharField(max_length=50)
