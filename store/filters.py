import django_filters
from store.models import Nft


class NftFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="cat__name", lookup_expr='iexact')

    class Meta:
        model = Nft
        fields = ['min_price', 'max_price', 'category']
