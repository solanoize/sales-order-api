from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'sku')
    list_filter = ('owner', 'created_at')
