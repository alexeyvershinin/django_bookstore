from django.contrib.auth.models import User, Group
from django.test import TestCase

from library.models import Book, Reviews
from library.utils import *


# Тесты метода проверки, принадлежит ли пользователь к группе работников магазина
class UserDroupTestCase(TestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('michal', 'password')
        self.test_user_2 = User.objects.create_user('tomas', 'password')

    # Пользователь принадлежит к группе 'employee'
    def test_user_group_ok(self):
        new_group, created = Group.objects.get_or_create(name='employee')
        new_group.user_set.add(self.test_user_1)
        result = is_employee(self.test_user_1)
        self.assertTrue(True, result)

    # Пользователь не принадлежит к группе 'employee'
    def test_user_group_false(self):
        result = is_employee(self.test_user_2)
        self.assertFalse(False, result)

# Тесты метода вычисления среднего рейтинга книг
class RaitingBookTestCase(TestCase):
    def test_raiting_book_ok(self):
        test_user_1 = User.objects.create_user('michal', 'password')
        test_user_2 = User.objects.create_user('tomas', 'password')
        book_1 = Book.objects.create(title='Книга_1', num_pages=100, cover_type='мягкая', price=500, pub_date=2020)
        review_1 = Reviews.objects.create(book_connected=book_1, author=test_user_1, content="отзыв_1", raiting=4)
        review_2 = Reviews.objects.create(book_connected=book_1, author=test_user_2, content="отзыв_2", raiting=5)
        reviews_connected = Reviews.objects.filter(
            book_connected=book_1)
        result = raiting_book(reviews_connected)
        self.assertEqual(4, result)

    def test_not_raiting_book(self):
        book_1 = Book.objects.create(title='Книга_1', num_pages=100, cover_type='мягкая', price=500, pub_date=2020)
        reviews_connected = Reviews.objects.filter(
            book_connected=book_1)
        result = raiting_book(reviews_connected)
        self.assertEqual('у книги еще нет рейтинга', result)
