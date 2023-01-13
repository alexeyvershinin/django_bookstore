from django.urls import path

from .views import *

urlpatterns = [
    path('', cart_info, name='list_cart'),  # корзина
    path('add/<int:book_id>', cart_add, name='add_cart'),  # добавление книги в корзину
    path('remove/<int:book_id>', cart_remove, name='remove_cart'),  # удаление книги из корзины
    path('clear/', cart_clear, name='clear_cart'),  # очистка корзины

    path('ordering/', create_order, name='ordering'),  # оформление заказа
]
