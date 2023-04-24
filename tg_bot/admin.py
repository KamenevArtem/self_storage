from django.contrib import admin
from django.contrib.auth.models import User

from .models import Box, Order, Customer, UserProfile
from django.contrib.auth.admin import UserAdmin


class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'size',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'conformation', 'order_end_date',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Order, OrderAdmin)
