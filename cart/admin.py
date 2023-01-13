from django.contrib import admin

from cart.models import Order_address, Order, Pos_order


# Register your models here.
class Order_addressAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'email', 'phone', 'city', 'zip_code', )
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'email')
    # поля по которым будет производиться поиск
    search_fields = ('email', 'phone', 'city', 'zip_code',)

# регистрирум модель и наш класс настроек
admin.site.register(Order_address, Order_addressAdmin)


# регистрирум модель и наш класс настроек
admin.site.register(Order)

class Pos_orderAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'order', 'book', 'count_book', 'price')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('order',)

admin.site.register(Pos_order, Pos_orderAdmin)