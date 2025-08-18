from django.contrib import admin
from django.db import models
from django.db.models import Avg
from django.utils.html import format_html

from apps.product_catalog.models import Category,Tag,Product
from apps.review.admin import ReviewInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'product_count')
    list_filter = ('parent',)
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_product_count=models.Count('products'))

    def product_count(self, obj):
        return obj._product_count

    product_count.admin_order_field = '_product_count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'product_count')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    actions = ['activate_tags', 'deactivate_tags']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_product_count=models.Count('product'))

    def product_count(self, obj):
        return obj._product_count

    product_count.admin_order_field = '_product_count'

    @admin.action(description='Activate selected tags')
    def activate_tags(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected tags')
    def deactivate_tags(self, request, queryset):
        queryset.update(is_active=False)





@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'is_active',
        'average_rating',
        'tag_list'
    )
    list_filter = ('category', 'tags', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')
    filter_horizontal = ('tags',)
    inlines = [ReviewInline]
    readonly_fields = ('created_at', 'updated_at')
    actions = ['activate_products', 'deactivate_products']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('tags').annotate(
            _average_rating=Avg('reviews__rating')
        )

    def average_rating(self, obj):
        return round(obj._average_rating, 2) if obj._average_rating else "N/A"

    average_rating.admin_order_field = '_average_rating'

    def tag_list(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all()[:3])

    @admin.action(description='Activate selected products')
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected products')
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)

