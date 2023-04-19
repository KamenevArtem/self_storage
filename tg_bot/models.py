from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Box(models.Model):
    hight = models.FloatField(
        verbose_name="Высота бокса",
        null=True
    )
    length = models.FloatField(
        verbose_name="Длина бокса",
        null=True
    )
    width = models.FloatField(
        verbose_name="Ширина бокса",
        null=True
    )
    rental_price = models.PositiveBigIntegerField(
        verbose_name="Стоимость суточной аренды",
        null=True
    )

class Order(models.Model):
    box = models.ForeignKey(
        Box,
        verbose_name="Номер бокса",
        related_name='boxes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    order_start_date = models.DateField(
        verbose_name="Дата начала контракта",
        blank=True
    )
    order_end_date = models.DateField(
        verbose_name="Дата закрытия заказа",
        blank=True
    )
    cargo_size = models.FloatField(
        verbose_name="Объём груза"
    )
    cargo_weight = models.FloatField(
        verbose_name="Вес груза"
    )


class Customer(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="ID пользователя"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
        blank=True,
        db_index=True
    )
    phone_number = PhoneNumberField(
        verbose_name = "Номер телефона",
        blank=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        verbose_name="Заказы",
        null=True,
        blank=True,
        related_name='customers'
    )

