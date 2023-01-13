import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied, BadRequest

from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework import permissions, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .forms import BookCreateForm, UserLoginForm, UserRegistrationForm, ReviewsForm, ContactForm, AuthorCreateForm
from .models import Book, Genre, Reviews, Author
from .serializers import BookListSerializer, AuthorListSerializer, BookDetailSerializer, AuthorDetailSerializer, \
    GenresListSerializer, ReviewsCreateSerializer, AuthorCreateSerializer, ReviewsDeleteSerializer, BookCreateSerializer
from .utils import is_employee, raiting_book
from cart.forms import CartAddProductForm


# Create your views here.

# поскольку на главной странице мы не используем обращение к базе данных,
# то использовать классы нецелесеобразно
def index(request):
    return render(request, 'library/index.html')


'''Блок книг'''


# определяем класс вывода списка книг
# на странице Каталог книг не требуется передавать дополнительную
# динамичеки-изменяемую информацию в шаблон, поэтому используем extra_content
class BooksList(ListView):
    model = Book
    template_name = 'library/books/books_list.html'
    context_object_name = 'books'
    paginate_by = 6
    extra_context = {
        'title': 'каталог книг',
    }

    def get_queryset(self):
        return Book.objects.all().order_by('title')


# определяем класс вывода подробной информации о книге
class DetailBookView(DetailView):
    model = Book
    template_name = 'library/books/book_detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'
    extra_context = {
        'title': 'каталог книг',
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        reviews_connected = Reviews.objects.filter(
            book_connected=self.get_object()).order_by('-date_posted')
        data['reviews'] = reviews_connected
        data['book_raiting'] = raiting_book(reviews_connected)
        data['form_cart'] = CartAddProductForm()

        if self.request.user.is_authenticated:
            data['reviews_form'] = ReviewsForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_review = Reviews(content=request.POST.get('content'),
                             author=self.request.user,
                             book_connected=self.get_object())
        new_review.save()
        messages.success(request, 'Ваш отзыв успешно добавлен')
        return self.get(self, request, *args, **kwargs)


# Класс получения списка книг по жанрам
class BooksByGenre(ListView):
    model = Book
    template_name = 'library/books/books_genre.html'
    context_object_name = 'books'
    paginate_by = 6

    # для передачи динамически-изменяемых данных используем метод get_context_data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Genre.objects.get(pk=self.kwargs['genre_id'])
        return context

    # переопределим метод Queryset
    def get_queryset(self):
        return Book.objects.filter(genres=self.kwargs['genre_id'])


# определяем класс Создания новой записи о книге
class BookCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'library.add_book'
    login_url = 'user_login'
    model = Book
    form_class = BookCreateForm
    template_name = 'library/books/book_add.html'
    context_object_name = 'form'
    extra_context = {
        'title': 'каталог книг/Новая запись'
    }
    success_url = reverse_lazy('employee_book_list')
    success_message = 'Книга успешно добавлена'


# определяем класс Редактирования записи о книге
class BookUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'library.change_book'
    login_url = 'user_login'
    model = Book
    form_class = BookCreateForm
    template_name = 'library/books/book_edit.html'
    context_object_name = 'form'
    success_url = reverse_lazy('employee_book_list')
    success_message = 'Запись успешно обновлена'
    extra_context = {
        'title': 'каталог книг/Редактирование зеписи'
    }


# определяем класс Удаления записи о книги
class BookDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'library.delete_book'
    login_url = 'user_login'
    model = Book
    success_url = reverse_lazy('employee_book_list')
    success_message = 'Книга успешно удалена'
    template_name = 'library/books/book_delete.html'


'''Блок поиска книг по сайту'''


# Определяем класс поиска
class Search(ListView):
    template_name = 'library/books/books_list.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.filter(
            Q(title__icontains=self.request.GET.get('q')) | Q(description__icontains=self.request.GET.get('q')) | Q(
                owner__full_name__icontains=self.request.GET.get('q')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        context['query_search'] = f'Результаты поиска по запросу {self.request.GET.get("q")}'
        return context


'''Блок методов аутентификации пользователя'''


# Авторизация
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('books_list')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'title': 'Авторизация'
    }
    return render(request, 'auth/login.html', context)


# Регистрация
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('user_login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'auth/register.html', context)


# Логаут
def user_logout(request):
    logout(request)
    return redirect('user_login')


'''Блок обратной связи'''


# Определяем метод обратной связи
def feedback(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = ''
            message += f'От пользователя: {request.user}\n'
            message += f'Email для обратной связи: {form.cleaned_data["contact"]}\n'
            message += f'Сообщение:\n'
            message += f'{form.cleaned_data["content"]}'
            mail = send_mail(form.cleaned_data['subject'], message, settings.EMAIL_HOST_USER, ['og2001@yandex.ru'],
                             fail_silently=False)
            if mail:
                messages.success(request, 'Сообщение успешно отправлено')
                return redirect('feedback')
            else:
                messages.error(request, 'Ошибка отправки сообщения')
        else:
            messages.error(request, 'Ошибка валидации, проверьте правильность заполнения формы')
    else:
        form = ContactForm()
    context = {
        'form': form,
        'title': 'Обратная связь',
    }

    return render(request, 'library/feedback.html', context)


'''Блок авторов книг'''


# список авторов
class AuthorsList(ListView):
    model = Author
    template_name = 'library/author/authors_list.html'
    context_object_name = 'authors'
    paginate_by = 6
    extra_context = {
        'title': 'Список авторов',
    }

    def get_queryset(self):
        return Author.objects.all().order_by('full_name')


# подробная информация об авторе
class DetailAuthorView(DetailView):
    model = Author
    template_name = 'library/author/author_detail.html'
    context_object_name = 'author'
    pk_url_kwarg = 'author_id'
    extra_context = {
        'title': 'Информация об авторе',
    }


# определяем класс Создания автора
class AuthorCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'library.add_author'
    login_url = 'user_login'
    model = Author
    form_class = AuthorCreateForm
    template_name = 'library/author/author_add.html'
    context_object_name = 'form'
    extra_context = {
        'title': 'Список авторов/Новая запись'
    }
    success_url = reverse_lazy('employee_author_list')
    success_message = 'Автор успешно добавлен'


# определяем класс Редактирования записи об авторе
class AuthorUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'library.change_author'
    login_url = 'user_login'
    model = Author
    form_class = AuthorCreateForm
    template_name = 'library/author/author_edit.html'
    context_object_name = 'form'
    success_url = reverse_lazy('employee_author_list')
    success_message = 'Запись успешно обновлена'
    extra_context = {
        'title': 'Список авторов/Редактирование зеписи'
    }


# определяем класс удаления автора
class AuthorDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'library.delete_author'
    login_url = 'user_login'
    model = Author
    success_url = reverse_lazy('employee_author_list')
    success_message = 'Автор успешно удален'
    template_name = 'library/author/author_delete.html'


'''Блок служебной страницы'''


# служебная страница
class EmployeeView(PermissionRequiredMixin, TemplateView):
    permission_required = 'library.add_book'
    login_url = 'user_login'
    template_name = 'library/employee/employee.html'
    extra_context = {
        'title': 'Служебная страница'
    }


# Список книг служебная страница
class EmployeeBooksList(PermissionRequiredMixin, ListView):
    permission_required = 'library.add_book'
    login_url = 'user_login'
    model = Book
    template_name = 'library/employee/employee_books_list.html'
    context_object_name = 'books'
    paginate_by = 8
    extra_context = {
        'title': 'Cлужебная страница/Каталог книг',
    }

    def get_queryset(self):
        return Book.objects.all().order_by('title')


# Список авторов служебная страница
class EmployeeAuthorList(PermissionRequiredMixin, ListView):
    permission_required = 'library.add_author'
    login_url = 'user_login'
    model = Author
    template_name = 'library/employee/employee_author_list.html'
    context_object_name = 'authors'
    paginate_by = 8
    extra_context = {
        'title': 'Cлужебная страница/Список авторов',
    }

    def get_queryset(self):
        return Author.objects.all().order_by('full_name')


'''Блок кастомных ошибок'''


# переопределяем шаблоны ошибок
def custom_permission_denied_view(request, exception=None):
    context = dict()
    context['title'] = '403 В доступе отказано'
    response = render(request, "error/403.html", context)
    response.status_code = 403
    return response


def custom_page_not_found_view(request, exception):
    context = dict()
    context['title'] = '404 Страница не найдена'
    response = render(request, "error/404.html", context)
    response.status_code = 404
    return response


def custom_error_view(request, exception=None):
    context = dict()
    context['title'] = '500 Ошибка сервера'
    response = render(request, "error/500.html", context)
    response.status_code = 500
    return response


def custom_bad_request_view(request, exception=None):
    context = dict()
    context['title'] = '400 Неверный запрос'
    response = render(request, "error/400.html", context)
    response.status_code = 400
    return response


# Вызываем ошибки
def permission_denied_view(request):
    raise PermissionDenied


def page_not_found_view(request):
    raise Http404


def bad_request_view(request):
    raise BadRequest


def server_error_view(request):
    raise Exception('Make response code 500!')


'''Блок APi'''


# Пользовательский класс разрешений, предоставляет права администратору или работникам магазина
class IsAdminOrEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff or is_employee(request.user))


class BookAPIListView(generics.ListAPIView):
    '''Вывод списка книг'''
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['title', ]


class BookAPIDetailView(generics.RetrieveAPIView):
    '''Вывод подробной информации о книге'''
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = (IsAuthenticated,)


class BookAPICreateView(generics.CreateAPIView):
    '''Добавление новой книги'''
    serializer_class = BookCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminOrEmployee,)


class BookAPIUpdateView(generics.UpdateAPIView):
    '''Редактирование записи о книге'''
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminOrEmployee,)


class BookAPIDeleteView(generics.DestroyAPIView):
    '''Удаление записи о книге'''
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = (IsAdminUser,)


class AuthorAPIListView(generics.ListAPIView):
    '''Вывод списка авторов'''
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = (IsAuthenticated,)


class AuthorAPIDetailView(generics.RetrieveAPIView):
    '''Вывод подробной информации об авторе'''
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = (IsAuthenticated,)


class AuthorAPICreateView(generics.CreateAPIView):
    '''Добавление нового автора'''
    serializer_class = AuthorCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminOrEmployee,)


class AuthorAPIUpdateView(generics.UpdateAPIView):
    '''Редактирование записи об авторе'''
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminOrEmployee,)


class AuthorAPIDeleteView(generics.DestroyAPIView):
    '''Удаление записи об авторе'''
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer
    permission_classes = (IsAdminUser,)


class GenresAPIListView(generics.ListAPIView):
    '''Вывод списка жанров книг'''
    queryset = Genre.objects.all()
    serializer_class = GenresListSerializer
    permission_classes = (IsAuthenticated,)


class GenresAPICreateView(generics.CreateAPIView):
    '''Добавление нового жанра книги'''
    serializer_class = GenresListSerializer
    permission_classes = (IsAuthenticated, IsAdminOrEmployee,)


class GenresAPIUpdateView(generics.UpdateAPIView):
    '''Редактирование записи о жанре книги'''
    queryset = Genre.objects.all()
    serializer_class = GenresListSerializer
    permission_classes = (IsAuthenticated, IsAdminOrEmployee,)


class GenresAPIDeleteView(generics.DestroyAPIView):
    '''Удаление записи о жанре книги'''
    queryset = Genre.objects.all()
    serializer_class = GenresListSerializer
    permission_classes = (IsAdminUser,)


class ReviewsAPICreateView(generics.CreateAPIView):
    '''Добавление отзывов к книге'''
    serializer_class = ReviewsCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, date_posted=datetime.datetime.now())


class ReviewsAPIDeleteView(generics.DestroyAPIView):
    '''Удаление записи о жанре книги'''
    queryset = Reviews.objects.all()
    serializer_class = ReviewsDeleteSerializer
    permission_classes = (IsAdminUser,)
