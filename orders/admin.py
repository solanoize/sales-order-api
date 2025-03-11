from django.contrib import admin

from orders.models import SalesOrder


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('status', 'total_amount', 'order_date', 'owner')
    # search_fields = ('customer__first_name', 'customer__last_name')
    list_filter = ('status', 'order_date')

