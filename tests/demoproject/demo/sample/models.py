from django.db import models

from unicef_djangolib.fields import CurrencyField, QuarterField


class DemoModel(models.Model):
    name = models.CharField(max_length=50)
    boolean_field = models.BooleanField(default=False)
    currency = CurrencyField()
    quarter = QuarterField()

