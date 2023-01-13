from .models import Book, Reviews, Author, Genre
from rest_framework import serializers

# Сериалайзеры
class ReviewsSerializer(serializers.ModelSerializer):
    '''Вывод отзывов к книгам'''
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Reviews
        exclude = ('book_connected',)


class ReviewsCreateSerializer(serializers.ModelSerializer):
    '''Добавление отзывов к книге'''

    class Meta:
        model = Reviews
        fields = ('content', 'raiting', 'book_connected')


class ReviewsDeleteSerializer(serializers.ModelSerializer):
    '''Удаление отзыва к книгам'''

    class Meta:
        model = Reviews
        fields = '__all__'


class AuthorListSerializer(serializers.ModelSerializer):
    '''Список авторов'''

    class Meta:
        model = Author
        fields = ('id', 'full_name')


class AuthorDetailSerializer(serializers.ModelSerializer):
    '''Подробная информация об авторе'''

    class Meta:
        model = Author
        exclude = ('photo',)


class AuthorCreateSerializer(serializers.ModelSerializer):
    '''Создание нового автора'''

    class Meta:
        model = Author
        fields = '__all__'


class GenresListSerializer(serializers.ModelSerializer):
    '''Список жанров книг'''

    class Meta:
        model = Genre
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    '''Список книг'''
    owner = AuthorListSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'owner')


class BookDetailSerializer(serializers.ModelSerializer):
    '''Подробная информация о книге'''
    genres = GenresListSerializer(read_only=True, many=True)
    owner = AuthorListSerializer(read_only=True)
    reviews = ReviewsSerializer(many=True)

    class Meta:
        model = Book
        exclude = ('photo_cover', 'photo_back')


class BookCreateSerializer(serializers.ModelSerializer):
    '''Создание новой книги'''

    class Meta:
        model = Book
        fields = '__all__'
