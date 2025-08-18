from django_filters import rest_framework as filters

from apps.product_catalog.models import Product


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    tags = filters.CharFilter(field_name='tags__name', lookup_expr='iexact', method='filter_tags')

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value.split(','))

    class Meta:
        model = Product
        fields = ['category', 'tags']