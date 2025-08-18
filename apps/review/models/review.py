from django.conf import settings
from django.contrib.auth.models import User
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
    )
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=0
    )
    comment = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product_review',
                violation_error_message='You have already reviewed this product'
            )
        ]
    def __str__(self):
        return f"Review for {self.product.name} ({self.rating})"

    def save(self, *args, **kwargs):
        """Handle approval status changes"""
        if self.pk:  # Existing review being updated
            old = Review.objects.get(pk=self.pk)
            if old.approved != self.approved:
                super().save(*args, **kwargs)
                self.product.update_rating_cache()
                return

        super().save(*args, **kwargs)