from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),  # домашняя страница

    # Книги
    path('books/', BooksList.as_view(), name='books_list'),  # Каталог книг
    path('books/<int:book_id>/', DetailBookView.as_view(), name='detail_books'),  # Подробная информация о книге
    path('genre/<int:genre_id>/', BooksByGenre.as_view(), name='genre'),  # Вывод списка книг по жанрам
    path('books/add_book/', BookCreate.as_view(), name='add_book'),  # Добавление новой книги
    path('books/edit/<int:pk>/', BookUpdate.as_view(), name='edit_book'),  # Редактирование записи о книги
    path('books/delete/<int:pk>/', BookDelete.as_view(), name='delete_book'),  # Удаление книги

    # Поиск книг по сайту
    path('search/', Search.as_view(), name='search'),  # Поиск

    # Аутентификация пользователя
    path('login/', user_login, name='user_login'),  # Авторизация
    path('logout/', user_logout, name='user_logout'),  # Логаут
    path('register/', user_register, name='user_register'),  # Регистрация
    # Обратная связб с магазином
    path('contact/', feedback, name='feedback'),  # Обратная связь

    # Авторы книг
    path('authors/', AuthorsList.as_view(), name='authors_list'),  # Список авторов
    path('authors/<int:author_id>/', DetailAuthorView.as_view(), name='detail_author'),
    # Подробная информация об авторе
    path('authors/add_author/', AuthorCreate.as_view(), name='add_author'),  # Добавление нового автора
    path('authors/edit/<int:pk>/', AuthorUpdate.as_view(), name='edit_author'),  # Редактирование записи об авторе
    path('authors/delete/<int:pk>/', AuthorDelete.as_view(), name='delete_author'),  # Удаление автора

    # Служебные страницы для работников магазина
    path('employee/', EmployeeView.as_view(), name='employee'),  # Служебная страница
    path('employee/book_list/', EmployeeBooksList.as_view(), name='employee_book_list'),  # Список книг для работников
    path('employee/author_list/', EmployeeAuthorList.as_view(), name='employee_author_list'),
    # Список авторов для работников

    # Маршруты для просмотра кастомных ошибок
    path('errors/403/', permission_denied_view),  # В доступе отказано
    path('errors/404/', page_not_found_view),  # Страница не найдена
    path('errors/400/', bad_request_view),  # Неверный запрос
    path('errors/500/', server_error_view),  # Ошибка сервера

    # API
    path('api/v1/auth/', include('rest_framework.urls')),  # подключение маршрута авторизации

    # Книги
    path('api/v1/books/', BookAPIListView.as_view(), name='api_books_list'),  # Вывод списка книг
    path('api/v1/books/<int:pk>/', BookAPIDetailView.as_view(), name='api_book_detail'),  # Подробная информация о книге
    path('api/v1/books/create/', BookAPICreateView.as_view(), name='api_book_create'),  # Создание новой книги
    path('api/v1/books/update/<int:pk>/', BookAPIUpdateView.as_view(), name='api_book_update'),  # Изменение записи о книге
    path('api/v1/books/delete/<int:pk>/', BookAPIDeleteView.as_view()),  # Удаление книги

    # Авторы
    path('api/v1/authors/', AuthorAPIListView.as_view()),  # Список авторов
    path('api/v1/authors/<int:pk>/', AuthorAPIDetailView.as_view()),  # Подробная информация об авторе
    path('api/v1/authors/create/', AuthorAPICreateView.as_view()),  # Создание нового автора
    path('api/v1/authors/update/<int:pk>/', AuthorAPIUpdateView.as_view()),  # Изменение сущетвующего автора
    path('api/v1/authors/delete/<int:pk>/', AuthorAPIDeleteView.as_view()),  # Удаление автора

    # Жанры
    path('api/v1/genres/', GenresAPIListView.as_view()),
    path('api/v1/genres/create/', GenresAPICreateView.as_view()),  # Создание нового жанра
    path('api/v1/genres/update/<int:pk>/', GenresAPIUpdateView.as_view()),  # Изменение сущетвующего жанра
    path('api/v1/genres/delete/<int:pk>/', GenresAPIDeleteView.as_view()),  # Удаление жанра

    # Отзывы к книгам
    path('api/v1/reviews/', ReviewsAPICreateView.as_view()),  # Создание отзыва к книге
    path('api/v1/reviews/delete/<int:pk>/', ReviewsAPIDeleteView.as_view()),  # Удаление отзыва о книге
]
