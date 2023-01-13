'''Блок дополнительных методов'''


# проверка, принадлежит ли пользователь к группе работников магазина
def is_employee(user):
    return user.groups.filter(name='employee').exists()


# Метод в котором возвращаем средний рейтинг книги на основе отзывов
def raiting_book(reviews_connected):
    try:
        start_raiting = 0
        for item in reviews_connected.values():
            start_raiting += item['raiting']
        return (start_raiting / reviews_connected.count()).__round__(0)
    except:
        return str('у книги еще нет рейтинга')
