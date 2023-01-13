from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Reviews, Author

'''Формы для отправки данных'''


# форма создания книги
class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'owner', 'description', 'num_pages', 'cover_type', 'price', 'pub_date', 'sizes',
                  'photo_cover', 'photo_back', 'genres']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*поле обязательно для заполнения'}),
            'owner': forms.Select(
                attrs={'class': 'form-control', 'placeholder': '*поле обязательно для заполнения'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'num_pages': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*поле обязательно для заполнения'}),
            'cover_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*поле обязательно для заполнения'}),
            'pub_date': forms.Select(attrs={'class': 'form-control'}),
            'sizes': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_cover': forms.FileInput(attrs={'class': 'form-control'}),
            'photo_back': forms.FileInput(attrs={'class': 'form-control'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


# форма создания Автора книги
class AuthorCreateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'biography', 'photo', 'birth_date', 'death_date']

        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*поле обязательно для заполнения'}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(
                attrs={"class": "form-control", 'placeholder': '*введите дату в формате "день.месяц.год"'}),
            'death_date': forms.DateInput(
                attrs={"class": "form-control", 'placeholder': '*если автор жив, это поле заполнять не нужно'})
        }


# форма авторизации пользователя
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


# форма регистрации пользователя
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтвердите пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# форма Отзывов о книге
class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['content', 'raiting']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'raiting': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewsForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""


# форма обратной связи
class ContactForm(forms.Form):
    contact = forms.EmailField(label='Email для обратной связи', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email для обратной связи'}))
    subject = forms.CharField(label='Тема сообщения',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема сообщения'}))
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(
        attrs={'class': 'form-control', "rows": 5, 'placeholder': 'Сообщение'}))
