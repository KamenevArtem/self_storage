from django.contrib import admin
from .models import Box, Order, Customer
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'hight', 'length', 'width',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer','conformation', 'order_end_date',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Order, OrderAdmin)
