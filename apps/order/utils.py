from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.order.models.order import Order, OrderItem
from apps.product_catalog.models import Product


def process_order(order_items,user=None):
    with transaction.atomic():
        order = Order.objects.create(user=user)
        total_price = 0  # Renamed for clarity

        for item in order_items:
            product = Product.objects.select_for_update().get(pk=item['product_id'])
            quantity = item['quantity']

            # Validate stock before creating OrderItem
            if quantity > product.stock:
                raise ValidationError(
                    f"Insufficient stock for {product.name}. Available: {product.stock}"
                )

            # Create and save OrderItem first
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price  # Store price at time of purchase
            )

            # Update product stock
            product.stock -= quantity
            product.save()

            # Accumulate total price
            total_price += order_item.item_price  # Use property calculation

        # Update and save order with total price
        order.total_price = total_price
        order.save()
        return order