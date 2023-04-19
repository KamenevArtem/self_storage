from django.contrib import admin
from .models import Box, Order, Customer
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'hight', 'length', 'width',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customers', 'order_end_date',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order',)


admin.site.register(Box, BoxAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
