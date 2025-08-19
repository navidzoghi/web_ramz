from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.order.models import Order, OrderItem
from apps.order.utils import process_order
from apps.product_catalog.models import Product, Category

User = get_user_model()
import logging

logger = logging.getLogger(__name__)
# Create your tests here.
class OrderProcessingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        logger.info(f'user: {self.user}')
        # Create category and products (with user where needed)
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.p1 = Product.objects.create(
            name="Test1", price=10, stock=5, category=self.category, slug="test1"
        )
        self.p2 = Product.objects.create(
            name="Test2", price=20, stock=3, category=self.category, slug="test2"
        )


    def test_transaction_rollback_on_insufficient_stock(self):
        order_items = [
            {'product_id': self.p1.id, 'quantity': 3},
            {'product_id': self.p2.id, 'quantity': 5}  # Exceeds stock
        ]

        with self.assertRaises(ValidationError) as context:
            process_order(order_items,user=self.user)

        # Verify error message
        self.assertIn("Insufficient stock for Test2", str(context.exception))

        # Verify atomic rollback
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

        # Verify stock unchanged
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.assertEqual(self.p1.stock, 5)
        self.assertEqual(self.p2.stock, 3)

    def test_successful_order_processing(self):
        order_items = [
            {'product_id': self.p1.id, 'quantity': 2},
            {'product_id': self.p2.id, 'quantity': 1}
        ]

        order = process_order(order_items,user=self.user)
        # Verify order creation
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.total_price, (2 * 10) + (1 * 20))

        # Verify stock reduction
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.assertEqual(self.p1.stock, 3)
        self.assertEqual(self.p2.stock, 2)

        # Verify price locking in OrderItems
        item1 = order.items.get(product=self.p1)
        item2 = order.items.get(product=self.p2)
        self.assertEqual(item1.price, 10)
        self.assertEqual(item2.price, 20)