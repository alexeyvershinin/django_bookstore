from django import template
from django.contrib.auth.models import User
from django.db.models import Count
from library.views import *

register = template.Library()

'''Блок пользовательских тегов'''


# Получение списка жанров
@register.simple_tag(name='get_list_genre')
def get_allgenre():
    return Genre.objects.all().order_by('title')


# Количество пользователей зарегистрированных на сайте
@register.simple_tag(name='users_count')
def get_user_count():
    users_count = User.objects.all().count()
    return users_count


# Количество книг в каталоге
@register.simple_tag(name='books_count')
def get_book_count():
    books_count = Book.objects.all().count()
    return books_count


# Количество авторов книг
@register.simple_tag(name='authors_count')
def get_authors_count():
    authors_count = Author.objects.all().count()
    return authors_count


# Количество отзывов к книгам
@register.simple_tag(name='reviews_count')
def get_reviews_count():
    reviews_count = Reviews.objects.all().count()
    return reviews_count


# регистрируем пользовательский тег и передаем полученные объекты в шаблон
@register.inclusion_tag('tags/list_genre.html')
def show_genre():
    genre = Genre.objects.annotate(cnt=Count('book')).filter(
        cnt__gt=0).order_by('title')  # не выводим жанры в которых нет книг

    return {'genre': genre}
