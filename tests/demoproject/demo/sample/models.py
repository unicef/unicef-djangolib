from django.db import models

from unicef_djangolib.fields import CurrencyField, QuarterField


class DemoModel(models.Model):
    name = models.CharField(max_length=50)
    currency = CurrencyField()
    quarter = QuarterField()

