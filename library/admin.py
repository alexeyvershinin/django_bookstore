from django.contrib import admin

from .models import Book, Genre, Reviews, Author


# Register your models here.

# настроим отображение объектов модели Library в админке
class LibraryAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'title', 'owner', 'num_pages', 'cover_type', 'price', 'sizes', 'pub_date')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'title')
    # поля по которым будет производиться поиск
    search_fields = ('id', 'title', 'owner', 'price', 'pub_date')
    # поля которые будем использовать для фильтрации
    list_filter = ('owner', 'cover_type', 'pub_date')
    # горизонтальное отображение поля genres(связь многие ко многим)
    filter_horizontal = ['genres']


# регистрирум модель и наш класс настроек
admin.site.register(Book, LibraryAdmin)


# настроим отображение объектов модели Genre в админке
class GenreAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'title')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'title')
    # поля по которым будет производиться поиск
    search_fields = ('title',)
    # поля которые будем использовать для фильтрации
    list_filter = ('title',)


# регистрирум модель и наш класс настроек
admin.site.register(Genre, GenreAdmin)


# настроим отображение объектов модели Reviews в админке
class ReviewsAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'book_connected', 'author', 'date_posted')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('author', 'book_connected')
    # поля по которым будет производиться поиск
    search_fields = ('author',)


# регистрирум модель и наш класс настроек
admin.site.register(Reviews, ReviewsAdmin)


# настроим отображение объектов модели Reviews в админке
class AuthorAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'full_name', 'birth_date', 'death_date')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'full_name')
    # поля по которым будет производиться поиск
    search_fields = ('full_name',)
    # поля которые будем использовать для фильтрации
    list_filter = ('full_name',)


# регистрирум модель и наш класс настроек
admin.site.register(Author, AuthorAdmin)