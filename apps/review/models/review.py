from django.db import models

from apps.core.models import AbstractModel
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.product_catalog.models import Product


class Review(AbstractModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Review for {self.product.name} ({self.rating})"