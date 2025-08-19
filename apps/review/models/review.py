from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import F

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

    def update_product_rating(self, old_rating=None):
        """Atomically update product rating counters"""
        with transaction.atomic():
            # Lock the product row
            product = Product.objects.active().select_for_update().get(pk=self.product_id)

            # Handle different update scenarios
            if not self.is_active and self.is_deleted:  # Review deleted
                if self.approved:
                    Product.objects.filter(pk=product.pk).update(
                        rating_sum=F('rating_sum') - self.rating,
                        rating_count=F('rating_count') - 1
                    )

            elif self.approved:
                if old_rating is not None:  # Rating update
                    rating_delta = self.rating - old_rating
                    Product.objects.filter(pk=product.pk).update(
                        rating_sum=F('rating_sum') + rating_delta
                    )
                else:  # New approved review
                    Product.objects.filter(pk=product.pk).update(
                        rating_sum=F('rating_sum') + self.rating,
                        rating_count=F('rating_count') + 1
                    )

            elif old_rating is not None and self.pk:  # Approval status change
                # Was approved, now unapproved
                if Review.objects.filter(pk=self.pk, is_approved=True).exists():
                    Product.objects.filter(pk=product.pk).update(
                        rating_sum=F('rating_sum') - self.rating,
                        rating_count=F('rating_count') - 1
                    )
                # Was unapproved, now approved
                elif self.approved:
                    Product.objects.filter(pk=product.pk).update(
                        rating_sum=F('rating_sum') + self.rating,
                        rating_count=F('rating_count') + 1
                    )