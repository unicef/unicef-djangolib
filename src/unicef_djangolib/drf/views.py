import functools
import operator

from django.db.models import Q
from rest_framework.generics import GenericAPIView


class QueryStringFilterAPIView(GenericAPIView):
    """Mixin which allow to filter and search based on querystring filters"""
    search_param = 'search'
    filters = ()
    search_terms = ()

    def filter_params(self, filters=None):
        filters = filters or self.filters
        queries = []
        for param_filter, query_filter in filters:
            if param_filter in self.request.query_params:
                value = self.request.query_params.get(param_filter)
                if query_filter.endswith('__in'):
                    value = value.split(',')
                queries.append(Q(**{query_filter: value}))
        return queries

    def search_params(self, search_terms=None):
        search_terms = search_terms or self.search_terms
        search_term = self.request.query_params.get(self.search_param)
        search_query = Q()
        if self.search_param in self.request.query_params:
            for param_filter in search_terms:
                q = Q(**{param_filter: search_term})
                search_query = search_query | q
        return search_query

    def get_queryset(self):
        qs = super().get_queryset()

        query_params = self.request.query_params
        if query_params:
            queries = []
            queries.extend(self.filter_params())
            queries.append(self.search_params())

            if queries:
                expression = functools.reduce(operator.and_, queries)
                qs = qs.filter(expression)
        return qs
