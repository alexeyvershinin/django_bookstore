from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings

from library.models import Book
from .cart import Cart
from .forms import CartAddProductForm, AddressDeliveryForm
from django.views.decorators.http import require_POST

from .models import Order_address, Order, Pos_order

'''Блок корзины покупателя'''


# Mетод добавления книги в корзину
@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book_obj = get_object_or_404(Book, pk=book_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cart.add(book=book_obj,
                 count_book=form.cleaned_data['count_book'],
                 update_count=form.cleaned_data['update'])
    return redirect('list_cart')


# Метод удаления книги из корзины
def cart_remove(request, book_id):
    cart = Cart(request)
    book_obj = get_object_or_404(Book, pk=book_id)
    cart.remove(book=book_obj)
    messages.success(request, 'Товар успешно удален из корзины')
    return redirect('list_cart')


# Корзина покупателя
def cart_info(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'title': 'Корзина покупателя'
    }
    return render(request, 'cart/detail.html', context)


# Mетод очистки корзины
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Корзина была успешно очищена')
    return redirect('books_list')


'''Блок оформления заказа'''


def create_order(request):
    cart = Cart(request)
    data = {
        'cart': cart
    }
    if len(cart) > 0:
        if request.method == 'POST':
            form = AddressDeliveryForm(request.POST)
            if form.is_valid():
                address = Order_address.objects.create(city=form.cleaned_data['city'],
                                                       street=form.cleaned_data['street'],
                                                       house_number=form.cleaned_data['house_number'],
                                                       house_frame=form.cleaned_data['house_frame'],
                                                       flat=form.cleaned_data['flat'],
                                                       zip_code=form.cleaned_data['zip_code'],
                                                       email=form.cleaned_data['email'],
                                                       phone=form.cleaned_data['phone'])
                order = Order.objects.create(price=cart.get_total_full_price(),
                                             address_delivery=address)
                data['address'] = address
                data['order'] = order
                for item in cart:
                    Pos_order.objects.create(order=order,
                                             book=item['book'],
                                             price=item['total_price'],
                                             count_book=item['count_book'])
                messages.success(request, 'Ваш заказ успешно создан. Письмо с подтверждением отправлено Вам на почту')

                html_body = render_to_string('cart/email.html', data)
                msg = EmailMultiAlternatives(subject=f'Book_magazine. Информация по заказу №{order.pk}',
                                             from_email=settings.EMAIL_HOST_USER,
                                             to=[form.cleaned_data['email'], ])
                msg.attach_alternative(html_body, 'text/html')
                msg.send()

                cart.clear()
                return redirect('books_list')
            else:
                messages.error(request, 'Ошибка валидации, проверьте правильность заполнения формы')
        else:
            form = AddressDeliveryForm
        context = {
            'form': form,
            'title': 'Оформление заказа'
        }
        return render(request, 'cart/ordering.html', context)
    else:
        raise Http404
