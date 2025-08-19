from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from jsonschema.exceptions import ValidationError

from apps.core.models import AbstractModel
from apps.product_catalog.models import Product


class OrderStatus(models.TextChoices):
    PENDING= 'pending','Pending'
    PROCESSING= 'processing','Processing'
    COMPLETED= 'completed','Completed'
    FAILED= 'failed','Failed'


class Order(AbstractModel):
    status = models.CharField(max_length=15,choices=OrderStatus.choices,default=OrderStatus.PENDING)
    total_price = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


    def calculate_total_price(self, save=False):
        from django.db.models import Sum, F
        result = self.items.active().aggregate(
            total=Sum(F('price') * F('quantity')))
        total = result['total'] or 0
        self.total_price = total
        if save:
            self.save(update_fields=['total_price'])
        return total


class OrderItem(AbstractModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=20,decimal_places=2,default=0)

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError(f"Insufficient stock for {self.product.name}. Available: {self.product.stock}")


    def save(self, *args, **kwargs):
        if not self.pk:  # Only set price on initial creation(Avoid making Query to db)
            self.price = self.product.price
        super().save(*args, **kwargs)


    @property
    def item_price(self):
        return self.price * self.quantity
