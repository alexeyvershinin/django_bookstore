from django import forms
from django.core.exceptions import ValidationError

from cart.models import Order_address

PROD_MAX_COUNT = [(i, str(i)) for i in range(1, 21)]


# Форма добавления товара в корзину
class CartAddProductForm(forms.Form):
    count_book = forms.TypedChoiceField(choices=PROD_MAX_COUNT, coerce=int, label='Количество:')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


# Форма добавления адреса доставки
class AddressDeliveryForm(forms.ModelForm):
    class Meta:
        model = Order_address
        fields = '__all__'

        widgets = {
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*Введите название населенного пункта'}),
            'zip_code': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*Почтовый индекс'}),
            'street': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*Название улицы'}),
            'house_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*Номер дома'}),
            'house_frame': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Строение/корпус'}),
            'flat': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Квартира/офис'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*Номер телефона'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '*Email для обратной связи'}),
        }

    # Напишем дополнительные валидаторы
    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if zip_code in range(100000, 694924):
            return zip_code
        else:
            raise ValidationError('вы должны ввести правильный почтовый индекс')

    def clean_house_number(self):
        house_number = self.cleaned_data['house_number']
        if house_number.isdigit():
            return house_number
        else:
            raise ValidationError('Введите целое число')

    def clean_flat(self):
        flat = self.cleaned_data['flat']
        if flat is not None:
            if flat not in range(1, 10000):
                raise ValidationError('Длина поля не может превышать 4 символа')
            else:
                return flat
        else:
            return flat
