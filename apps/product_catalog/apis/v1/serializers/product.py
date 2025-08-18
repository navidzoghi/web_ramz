from rest_framework import serializers

from apps.product_catalog.models import Category, Tag, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uuid', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['uuid', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    average_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        read_only=True,
        source='avg_rating'
    )

    class Meta:
        model = Product
        fields = [
            'uuid', 'name', 'slug','description', 'price', 'stock',
            'category', 'tags', 'average_rating'
        ]
