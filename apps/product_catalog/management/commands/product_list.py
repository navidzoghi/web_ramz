'''
Optimization Explanation:
- Uses `select_related('category')` to fetch category data in the initial query (1 SQL query).
- Uses `Prefetch` with `Tag.objects.filter(active=True)` to fetch only active tags in a second query (1 SQL query).
- Uses `annotate(avg_rating=Avg('reviews__rating'))` to calculate average ratings in the initial query (1 SQL query).
Total: 3 SQL queries regardless of the number of products, avoiding N+1 queries.
'''

from django.core.management.base import BaseCommand
from django.db.models import Prefetch, Avg

from apps.product_catalog.models import Tag, Product


class Command(BaseCommand):
    help = 'Prints all products with related data efficiently'

    def handle(self, *args, **kwargs):
        # Prefetch only active tags using custom Prefetch queryset
        active_tags_prefetch = Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_active=True, is_deleted=False),
        )

        products = Product.objects.select_related('category') \
            .prefetch_related(active_tags_prefetch) \
            .annotate(avg_rating=Avg('reviews__rating'))

        for product in products:
            tag_names = ", ".join(tag.name for tag in product.tags.all())
            self.stdout.write(
                f"Product: {product.name}, "
                f"Price: {product.price}, "
                f"Category: {product.category.name}, "
                f"Tags: {tag_names}, "
                f"Avg Rating: {product.avg_rating or 'N/A'}"
            )