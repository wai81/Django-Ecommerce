from django.shortcuts import render, get_object_or_404

from category.models import Category
from .models import Product


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)  # получаем выбранныю категорию или код ошибки 404
        # фильтруем подукты с выбранной ктегорией и  фильтром if_available=True
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()  # count() возвращает количество записей
    else:
        products = Product.objects.all().filter(is_available=True)  # выбираем все подукты с фильтром if_available=True
        product_count = products.count()  # count() возвращает количество записей

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    return render(request, 'store/product_detail.html')
