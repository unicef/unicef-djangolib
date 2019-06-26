from django.contrib.contenttypes.fields import GenericRelation, ReverseGenericManyToOneDescriptor
from django.db import models
from django.utils.functional import cached_property
from model_utils import Choices

CURRENCY_LIST = [
    u'GIP', u'KPW', u'XEU', u'BHD', u'BIF', u'BMD', u'BSD', u'AFN', u'ALL', u'AMD', u'AUD', u'AZN', u'BAM',
    u'BBD', u'BDT', u'BZD', u'CUP1', u'BTN', u'ZWL', u'AWG', u'CUC', u'VEF01', u'BND', u'BRL', u'ARS', u'ETB', u'EUR',
    u'FJD', u'GBP', u'GEL', u'GHS', u'GNF', u'GTQ', u'GYD', u'HNL', u'CAD', u'CDF', u'CLP', u'CNY', u'COP', u'CRC',
    u'CUP', u'CVE', u'DJF', u'DKK', u'DOP', u'DZD', u'EGP', u'HRK', u'LVL', u'LYD', u'MAD', u'MGA', u'MKD', u'KWD',
    u'KYD', u'LBP', u'LKR', u'MDL', u'KZT', u'LRD', u'BOB', u'HKD', u'CHF', u'KES', u'MYR', u'NGN', u'KMF', u'SCR',
    u'SEK', u'TTD', u'PKR', u'NIO', u'RWF', u'BWP', u'JMD', u'TJS', u'UYU', u'RON', u'PYG', u'SYP', u'LAK', u'ERN',
    u'SLL', u'PLN', u'JOD', u'ILS', u'AED', u'NPR', u'NZD', u'SGD', u'JPY', u'PAB', u'ZMW', u'CZK', u'SOS', u'LTL',
    u'KGS', u'SHP', u'BGN', u'TOP', u'MVR', u'VEF02', u'TMT', u'GMD', u'MZN', u'RSD', u'MWK', u'PGK', u'MXN', u'XAF',
    u'VND', u'INR', u'NOK', u'XPF', u'SSP', u'IQD', u'SRD', u'SAR', u'XCD', u'IRR', u'KPW01', u'HTG', u'IDR', u'XOF',
    u'ISK', u'ANG', u'NAD', u'MMK', u'STD', u'VUV', u'LSL', u'SVC', u'KHR', u'SZL', u'RUB', u'UAH', u'UGX', u'THB',
    u'AOA', u'YER', u'USD', u'UZS', u'OMR', u'SBD', u'TZS', u'SDG', u'WST', u'QAR', u'MOP', u'MRU', u'VEF', u'TRY',
    u'ZAR', u'HUF', u'MUR', u'PHP', u'BYN', u'KRW', u'TND', u'MNT', u'PEN'
]

CURRENCIES = Choices(*[(c, c) for c in CURRENCY_LIST])


class CurrencyField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 4)
        kwargs['choices'] = CURRENCIES
        kwargs['null'] = kwargs.get('null', False)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['default'] = kwargs.get('default', '')
        super().__init__(*args, **kwargs)


class QuarterField(models.CharField):

    Q1 = 'q1'
    Q2 = 'q2'
    Q3 = 'q3'
    Q4 = 'q4'

    QUARTERS = Choices(
        (Q1, 'Q1'),
        (Q2, 'Q2'),
        (Q3, 'Q3'),
        (Q4, 'Q4')
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 2)
        kwargs['choices'] = self.QUARTERS
        kwargs['null'] = kwargs.get('null', True)
        kwargs['blank'] = kwargs.get('blank', True)
        super().__init__(*args, **kwargs)


def coded_create_reverse_many_to_one_manager(superclass, rel):
    class RelatedManager(superclass):
        def __init__(self, instance=None):
            super().__init__(instance)
            if rel.field.code:
                self.core_filters[rel.field.code_field] = rel.field.code

    return RelatedManager


class CodedReverseManyToOneDescriptor(ReverseGenericManyToOneDescriptor):
    @cached_property
    def related_manager_cls(self):
        return coded_create_reverse_many_to_one_manager(
            super().related_manager_cls, self.rel
        )


class CodedGenericRelation(GenericRelation):
    code = None
    code_field = None

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(
            cls,
            self.name,
            CodedReverseManyToOneDescriptor(self.remote_field)
        )

    def __init__(self, *args, **kwargs):
        self.code = kwargs.pop('code', self.code)
        self.code_field = kwargs.pop('code_field', 'code')
        super().__init__(*args, **kwargs)

    def get_extra_restriction(self, where_class, alias, remote_alias):
        cond = super().get_extra_restriction(where_class, alias, remote_alias)

        field = self.remote_field.model._meta.get_field(self.code_field)
        lookup = field.get_lookup('exact')(
            field.get_col(remote_alias),
            self.code
        )
        cond.add(lookup, 'AND')
        return cond
