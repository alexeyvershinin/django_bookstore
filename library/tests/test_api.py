import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Book, Author, Genre, Reviews
from library.serializers import BookListSerializer, BookDetailSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.author_1 = Author.objects.create(full_name='Автор_1', birth_date='1962-11-22')
        self.author_2 = Author.objects.create(full_name='Автор_2', birth_date='1982-05-19')
        self.genre_1 = Genre.objects.create(title="новинка")
        self.book_1 = Book.objects.create(title='Книга_1', num_pages=100, cover_type='мягкая', price=500, pub_date=2020,
                                          owner=self.author_1)
        self.book_2 = Book.objects.create(title='Книга_2', num_pages=160, cover_type='твердая', price=1000,
                                          pub_date=2022,
                                          owner=self.author_2)
        self.user = User.objects.create_user('michal', 'password')
        self.admin = User.objects.create_superuser('admin', 'password')

    # Тест статуса при обращению к списку книг, если пользователь аутентифицирован
    def test_get_book_list_status_200(self):
        self.client.force_login(self.user)
        url = reverse('api_books_list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    # Тест статуса при обращению к списку книг, если пользователь не аутентифицирован
    def test_get_book_list_status_403(self):
        url = reverse('api_books_list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    # Тест получения списка книг
    def test_get_books_list(self):
        self.client.force_login(self.user)
        url = reverse('api_books_list')
        response = self.client.get(url)
        serializer_data = BookListSerializer([self.book_1, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # Тест получения создания книги
    def test_book_create(self):
        self.client.force_login(self.admin)
        self.assertEqual(2, Book.objects.all().count())
        url = reverse('api_book_create')
        data = {
            "title": "KG+",
            "description": "",
            "num_pages": 560,
            "cover_type": "твердая",
            "price": "949.0",
            "sizes": "135x207 мм",
            "pub_date": 2022,
            "owner": self.author_1.id,
            "genres": [self.genre_1.id, ]
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Book.objects.all().count())
