from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.review.apis.v1.views.review import ReviewViewSet


app_name = 'v1'  # This is important for namespace support

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path("products/<str:product_slug>/", include(router.urls)),
]