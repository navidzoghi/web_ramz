from django.db.models import Avg, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.core.permissons import IsAdminOrReadOnly
from apps.product_catalog.filters import ProductFilter
from apps.product_catalog.models import Product, Tag
from apps.product_catalog.apis.v1.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    def get_queryset(self):
        # Prefetch only active tags using custom Prefetch queryset
        active_tags_prefetch = Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_active=True, is_deleted=False),
        )

        products = Product.objects.select_related('category') \
            .prefetch_related(active_tags_prefetch) \
            .annotate(avg_rating=Avg('reviews__rating'))
        return products