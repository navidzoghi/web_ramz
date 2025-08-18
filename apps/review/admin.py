from django.contrib import admin

from apps.review.models import Review


# Register your models here.
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('rating', 'comment', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'rating', 'created_at', 'truncated_comment')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'comment')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def truncated_comment(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment

    truncated_comment.short_description = 'Comment Preview'