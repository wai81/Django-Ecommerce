from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from carts.models import Cart, CartItem
from store.models import Product


# создаем ID корзины или получаем ID
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# создаем корзину
def add_cart(request, product_id):

    product = Product.objects.get(id=product_id)  # get product by ID

    try:
        # получаем ИД корзины
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        # создаем корзину если её нет
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        # увеличиваем количество продукта в корзине если он есть в корзине
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # добовляем продукт в корзину
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    return HttpResponse(cart_item.quantity)
    exit()
    # переходим в корзину redirect-перенаправляет
    # return redirect('cart')


def cart(request):
    return render(request, 'store/cart.html')
