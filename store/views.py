from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from .models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# фунция отображения списка продуктов с отбором по категории
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)  # получаем выбранныю категорию или код ошибки 404
        # фильтруем подукты с выбранной ктегорией и  фильтром if_available=True
        products = Product.objects.filter(category=categories, is_available=True)

        # Реализация пагинации
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        product_count = products.count()  # count() возвращает количество записей
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')  # выбираем все подукты с фильтром if_available=True

        # Реализация пагинации
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        product_count = products.count()  # count() возвращает количество записей

    context = {
        # 'products': products, # перерача всех данных
        'products': paged_products,  # перерача данных по условию пагинации
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


# фунция отоброжения деталей о выбраном продукте
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as ex:
        raise ex

    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }

    return render(request, 'store/product_detail.html', context)
