from django.contrib.contenttypes.fields import GenericRelation, ReverseGenericManyToOneDescriptor
from django.db import models
from django.utils.functional import cached_property
from model_utils import Choices

CURRENCY_LIST = [
    'GIP', 'KPW', 'XEU', 'BHD', 'BIF', 'BMD', 'BSD', 'AFN', 'ALL', 'AMD', 'AUD', 'AZN', 'BAM',
    'BBD', 'BDT', 'BZD', 'CUP1', 'BTN', 'ZWL', 'AWG', 'CUC', 'VEF01', 'BND', 'BRL', 'ARS', 'ETB', 'EUR',
    'FJD', 'GBP', 'GEL', 'GHS', 'GNF', 'GTQ', 'GYD', 'HNL', 'CAD', 'CDF', 'CLP', 'CNY', 'COP', 'CRC',
    'CUP', 'CVE', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'HRK', 'LVL', 'LYD', 'MAD', 'MGA', 'MKD', 'KWD',
    'KYD', 'LBP', 'LKR', 'MDL', 'KZT', 'LRD', 'BOB', 'HKD', 'CHF', 'KES', 'MYR', 'NGN', 'KMF', 'SCR',
    'SEK', 'TTD', 'PKR', 'NIO', 'RWF', 'BWP', 'JMD', 'TJS', 'UYU', 'RON', 'PYG', 'SYP', 'LAK', 'ERN',
    'SLL', 'PLN', 'JOD', 'ILS', 'AED', 'NPR', 'NZD', 'SGD', 'JPY', 'PAB', 'ZMW', 'CZK', 'SOS', 'LTL',
    'KGS', 'SHP', 'BGN', 'TOP', 'MVR', 'VEF02', 'TMT', 'GMD', 'MZN', 'RSD', 'MWK', 'PGK', 'MXN', 'XAF',
    'VND', 'INR', 'NOK', 'XPF', 'SSP', 'IQD', 'SRD', 'SAR', 'XCD', 'IRR', 'KPW01', 'HTG', 'IDR', 'XOF',
    'ISK', 'ANG', 'NAD', 'MMK', 'STD', 'VUV', 'LSL', 'SVC', 'KHR', 'SZL', 'RUB', 'UAH', 'UGX', 'THB',
    'AOA', 'YER', 'USD', 'UZS', 'OMR', 'SBD', 'TZS', 'SDG', 'WST', 'QAR', 'MOP', 'MRU', 'VEF', 'TRY',
    'ZAR', 'HUF', 'MUR', 'PHP', 'BYN', 'KRW', 'TND', 'MNT', 'PEN'
]

CURRENCIES = Choices(*[(c, c) for c in CURRENCY_LIST])


class CurrencyField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 5)
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

        def get_prefetch_queryset(self, *args, **kwargs):
            rel_qs, rel_obj_attr, instance_attr, single, cache_name, is_descriptor = (
                super().get_prefetch_queryset(*args, **kwargs))

            rel_qs = rel_qs.filter(**{rel.field.code_field: rel.field.code})
            return rel_qs, rel_obj_attr, instance_attr, single, cache_name, is_descriptor

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
