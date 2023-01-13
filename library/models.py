import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
# создадим модель Жанров книг
class Genre(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название жанра')

    # отобразим информацию об объекте класса в админке
    def __str__(self):
        return self.title

    # настраиваем отображение приложения в админке
    class Meta:
        verbose_name = 'Жанр книги'
        verbose_name_plural = 'Жанры книг'
        ordering = ['title']  # сортировка в админке

    # определяем метод, которым выстраиваем ссылку для получения книг по жанру
    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_id': self.pk})


# определяем выбор значений для поля cover_type
COVER_CHOISES = (
    ('мягкая', 'мягкая'),
    ('твердая', 'твердая')
)
# определяем выбор значений для поля pub_date
YEAR_CHOICES = [(y, y) for y in range(1800, datetime.date.today().year + 1)]


# создаем модель Книг
class Book(models.Model):
    # поле обязательно для заполнения и ставим ограничение в 255 символов
    title = models.CharField(max_length=250, verbose_name='Название книги')
    # поле описания, к заполнению необязательно
    description = models.TextField(null=True, blank=True, verbose_name='Описание книги')
    # т.к. Integer слишком большое поле и может хранить в себе отрицательные значения
    # нам достаточно Decimal, поставим ограничение на количество знаков, и уберем цифры после запятой
    num_pages = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Количество страниц')
    # поле выбора обложки, вынесем выбор значений в отдельный список
    cover_type = models.CharField(max_length=7, choices=COVER_CHOISES, default='твердая', verbose_name='Тип обложки')
    # поле цены книги, особых требований к нему нет
    price = models.FloatField(verbose_name='Цена')
    # в поле размера книги поставим ограничение на количество символов и  сделаем необязательным к заполнению
    sizes = models.CharField(max_length=50, null=True, blank=True, verbose_name='Размер книги/формат издания')
    # поскольку в дате публикации указывается только год, сделаем поле Integer с выбором значений,
    # по умолчанию установим текущий год
    pub_date = models.IntegerField(choices=YEAR_CHOICES,
                                   default=datetime.datetime.now().year, verbose_name='Год издания')

    # добавим поля для обложки книги, укажем допустимый тип загружаемых файлов
    photo_cover = models.ImageField(upload_to='image/%Y/%m/%d',
                                    validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                                    null=True, blank=True, verbose_name='Передняя обложка')
    photo_back = models.ImageField(upload_to='image/%Y/%m/%d',
                                   validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                                   null=True, blank=True, verbose_name='Задняя обложка')
    genres = models.ManyToManyField(Genre, verbose_name='Жанр книги')
    owner = models.ForeignKey('Author', on_delete=models.SET_NULL, verbose_name='Автор книги', null=True, blank=True)

    # отобразим информацию об объекте класса в админке
    def __str__(self):
        return self.title

    # настраиваем отображение приложения в админке
    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Каталог книг'
        ordering = ['title']  # сортировка в админке

    # определяем метод, которым выстраиваем ссылку для подробного описания книги и передаем ее в шаблон
    def get_absolute_url(self):
        return reverse('detail_books', kwargs={'book_id': self.pk})


RAITING_CHOICES = [(y, y) for y in range(1, 6)]


# модель Отзывов
class Reviews(models.Model):
    book_connected = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE, verbose_name='Книга')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отзыва')
    content = models.TextField(verbose_name='Отзыв')
    raiting = models.IntegerField(choices=RAITING_CHOICES,
                                  default=5, verbose_name='Рейтинг книги')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата размещения отзыва')

    def __str__(self):
        return str(self.author) + ', ' + self.book_connected.title[:40]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


# модель Автор
class Author(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='ФИО автора')
    biography = models.TextField(null=True, blank=True, verbose_name='краткая биография')
    photo = models.ImageField(upload_to='image/%Y/%m/%d',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                              null=True, blank=True, verbose_name='Портрет автора')
    birth_date = models.DateField(verbose_name='Дата рождения')
    death_date = models.DateField(null=True, blank=True, verbose_name='Дата смерти')

    def __str__(self):
        return self.full_name

    # определяем метод, которым выстраиваем ссылку для подробной информации об авторе и передаем ее в шаблон
    def get_absolute_url(self):
        return reverse('detail_author', kwargs={'author_id': self.pk})

    class Meta:
        verbose_name = 'Автор книги'
        verbose_name_plural = 'Авторы книг'
        ordering = ['full_name']


