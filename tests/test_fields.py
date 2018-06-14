from django.db import connection

from unicef_djangolib.fields import CurrencyField, QuarterField


def test_currency_field():

    f = CurrencyField()
    assert f.db_parameters(connection)['type'] == 'varchar(4)'
    assert not f.db_parameters(connection)['check']


def test_quarter_field():

    f = QuarterField()
    assert f.db_parameters(connection)['type'] == 'varchar(2)'
    assert not f.db_parameters(connection)['check']
