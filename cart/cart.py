from django.conf import settings
from library.models import Book

# класс Корзина
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        # Обновление ключа "cart" в сессии
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметка сессии в опции "измененный", для обновления и сохранения данных
        self.session.modified = True

    def add(self, book, count_book=1, update_count=False):
        book_pk = str(book.pk)

        # Проверка наличия продукта в корзине (если нет в корзине, то добавляем)
        if book_pk not in self.cart:
            self.cart[book_pk] = {
                'count_book': 0,
                'price_book': str(book.price)
            }

        # Обновление количества книг в корзине
        if update_count:
            self.cart[book_pk]['count_book'] = count_book
        else:
            self.cart[book_pk]['count_book'] += count_book

        # Сохранение корзины в сессию
        self.save()

    def remove(self, book):
        book_pk = str(book.pk)

        # Если удаляемый товар лежит в корзине, то очищаем его ключ (и данные о нём)
        if book_pk in self.cart:

            del self.cart[book_pk]

            self.save()

    def get_total_full_price(self):
        return round(sum(float(item['price_book']) * int(item['count_book']) for item in self.cart.values()), 2)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __len__(self):
        return sum(int(item['count_book']) for item in self.cart.values())

    def __iter__(self):
        # Получение первичных ключей
        list_book_pk = self.cart.keys()

        # Загрузка данных из БД
        list_book_obj = Book.objects.filter(pk__in=list_book_pk)

        # Копирование корзины для дальнейшей работы
        cart = self.cart.copy()
        # Перебор и добавление объектов(записей) из БД
        for book_obj in list_book_obj:
            cart[str(book_obj.pk)]['book'] = book_obj

        for item in cart.values():
            item['total_price'] = round(float(item['price_book']) * int(item['count_book']),2)

            yield item