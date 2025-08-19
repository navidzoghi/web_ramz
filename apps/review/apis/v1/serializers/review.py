from rest_framework import serializers

from apps.product_catalog.models import Product
from apps.review.models import Review


class AddReviewSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    # product = serializers.SlugRelatedField(slug_field="slug", queryset=Product.objects.active(),required=True)
    extra_kwargs = {
        'original_image': {'required': True},
    }
    class Meta:
        model = Review
        fields =['uuid',"rating","comment"]
        extra_kwargs = {
            'rating': {'required': True},
            'comment': {'required': False}
        }

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['uuid',"rating","comment"]

class UpdateReviewSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    class Meta:
        model = Review
        fields =['uuid',"rating","comment"]