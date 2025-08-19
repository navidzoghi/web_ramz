from itertools import product

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissons import IsAdminOrReadOnly
from apps.product_catalog.models import Product
from apps.review.apis.v1.serializers.review import AddReviewSerializer, ReviewSerializer,UpdateReviewSerializer
from apps.review.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    # Action-specific serializers
    action_serializers = {
        'create': AddReviewSerializer,
        'list': ReviewSerializer,
        'retrieve': ReviewSerializer,
        'partial_update': UpdateReviewSerializer,
    }
    http_method_names = ['get', 'post', 'delete','patch']  # Only allow these methods
    lookup_field = 'uuid'
    def get_serializer_class(self):
        return self.action_serializers.get(self.action, ReviewSerializer)

    def get_queryset(self):
        # Get product slug from URL parameters
        product_slug = self.kwargs.get('product_slug')

        # Base queryset
        queryset = Review.objects.active().select_related(
            'user', 'product'
        ).order_by('-created_at')

        # Filter by product if slug is provided
        if product_slug:
            queryset = queryset.filter(product__slug=product_slug)

        return queryset

    def get_product_from_url(self):
        """Helper to get product from URL slug"""
        product_slug = self.kwargs.get('product_slug')
        if product_slug:
            return get_object_or_404(Product, slug=product_slug)
        return None
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Add Review with rate and comment"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Get the product from the validated data
        product = self.get_product_from_url()
        # Check if user already reviewed this product
        if Review.objects.filter(user=self.request.user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product")

        # Save the review
        review = serializer.save(user=self.request.user, product=product)
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Delete Review"""
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

