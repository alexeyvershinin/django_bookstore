from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from library.models import Book


# Create your models here.
# Создадим модель адреса доставки заказа
class Order_address(models.Model):
    city = models.CharField(max_length=150, verbose_name='Город')
    street = models.CharField(max_length=150, verbose_name='Улица')
    house_number = models.CharField(max_length=3, verbose_name='Номер дома')
    house_frame = models.CharField(max_length=1, null=True, blank=True, verbose_name='Корпус дома')
    flat = models.PositiveIntegerField(null=True, blank=True, verbose_name='Квартира')
    zip_code = models.PositiveIntegerField(verbose_name='Почтовый индекс')
    email = models.EmailField(verbose_name='Email')
    phone = PhoneNumberField(verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Адрес доставки заказа'
        verbose_name_plural = 'Адрес доставки заказа'


class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    date_finish = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения заказа")
    price = models.FloatField(null=True, verbose_name="Стоимость заказа")
    address_delivery = models.OneToOneField(Order_address, on_delete=models.CASCADE, primary_key=True, verbose_name='Адрес доставки')
    status = models.CharField(max_length=150, choices=[
        ('Создан', 'Создан'),
        ('Отменен', 'Отменен'),
        ('Согласован', 'Согласован'),
        ('В пути', 'В пути'),
        ('Завершен', 'Завершен'),
    ], default='Создан', verbose_name="Статус")

    books = models.ManyToManyField(Book, through='Pos_order',
                                    verbose_name='Книги')  # создание связи многие ко многим через таблицу Pos_order

    def __str__(self):
        return f'Заказ №{self.pk} от {(self.date_create).strftime("%b %d, %Y")} доставка для {self.address_delivery.email}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-pk']

class Pos_order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="Книга")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    count_book = models.IntegerField(verbose_name="Кол-во книг в заказе")
    price = models.FloatField(verbose_name="Общая стоимость книг")

    class Meta:
        verbose_name = 'Позицию в заказе'
        verbose_name_plural = 'Позиции в заказе'