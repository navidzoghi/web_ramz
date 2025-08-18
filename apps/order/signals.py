from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.order.models.order import OrderItem


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    instance.order.calculate_total_price(save=True)