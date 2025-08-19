from django.contrib import admin

from apps.order.models.order import OrderItem, Order


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Show one empty form by default
    fields = ('product', 'quantity', 'item_price')
    readonly_fields = ('item_price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('total_price',)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()  # Save OrderItems first
        formset.save_m2m()
        form.instance.calculate_total_price(save=True)  # Update order total


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'item_price')
    list_filter = ('order__status',)