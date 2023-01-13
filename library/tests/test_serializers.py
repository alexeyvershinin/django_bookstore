from django.test import TestCase

from library.models import Book, Author
from library.serializers import BookListSerializer, AuthorListSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self):
        author_1 = Author.objects.create(full_name='Автор_1', birth_date='1962-11-22')
        author_2 = Author.objects.create(full_name='Автор_2', birth_date='1982-05-19')
        book_1 = Book.objects.create(title='Книга_1', num_pages=100, cover_type='мягкая', price=500, pub_date=2020,
                                     owner=author_1)
        book_2 = Book.objects.create(title='Книга_2', num_pages=160, cover_type='твердая', price=1000, pub_date=2022,
                                     owner=author_2)
        data = BookListSerializer([book_1, book_2], many=True).data
        expexted_data = [
            {
                "id": book_1.id,
                "title": book_1.title,
                "owner": {
                    "id": author_1.id,
                    "full_name": author_1.full_name
                }},
            {
                "id": book_2.id,
                "title": book_2.title,
                "owner": {
                    "id": author_2.id,
                    "full_name": author_2.full_name
                }}
        ]
        self.assertEqual(expexted_data, data)


class AuthorSerializerTestCase(TestCase):
    def test_ok(self):
        author_1 = Author.objects.create(full_name='Автор_1', birth_date='1962-11-22')
        author_2 = Author.objects.create(full_name='Автор_2', birth_date='1982-05-19')
        data = AuthorListSerializer([author_1, author_2], many=True).data
        expexted_data = [
            {
                "id": author_1.id,
                "full_name": author_1.full_name
            },
            {
                "id": author_2.id,
                "full_name": author_2.full_name
            },

        ]
        self.assertEqual(expexted_data, data)
