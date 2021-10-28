import django_filters as filters
from django.db.models import Q
from logistic.models import Stock


class StockFilter(filters.FilterSet):
    products = filters.CharFilter(method='two_filds_filter',
                                  lookup_expr='contains',
                                  )

    class Meta:
        model = Stock
        fields = {'products'}

    def two_filds_filter(self, queryset, name, value):
        if value.isdigit():
            return Stock.objects.filter(Q(products__id=value))
        else:
            return Stock.objects.filter(
                Q(products__title__icontains=value) |
                Q(products__description__icontains=value)
             )
