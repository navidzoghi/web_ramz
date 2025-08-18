from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.product_catalog.apis.v1.views.product import ProductViewSet

app_name = 'v1'  # This is important for namespace support
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]