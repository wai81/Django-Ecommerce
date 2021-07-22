# создаем словарь с категориями для вывода в меню категории
from .models import Category


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
