from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Cart, CartItem
from store.models import Product, Variation
from django.contrib.auth.decorators import login_required


# создаем ID корзины или получаем ID
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# создаем корзину
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product
    # добавление в корзину если пользователь авторизирован
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product,
                                                      variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []  # пременная для передачи сущестующих характеристик продука
            id = []  # переменная для хранения id продукта
            # выгружаем список характеристик в ex_var_list
            for item in cart_item:
                exist_variation = item.variations.all()
                ex_var_list.append(list(exist_variation))  # передаем характеристики продукта
                id.append(item.id)  # передаем id продукта
            # проверяем есть ли продукт с такимиже характеристиками в корзине
            if product_variation in ex_var_list:
                # return HttpResponse('True')
                # увеличиваем количество продукта в корзине
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # добавляем продукт в корзину
                # добавляем характеристик продукта в корзину
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            # добовляем продукт в корзину
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            # добавляем характеристик продукта в карзину
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        # переходим в корзину redirect-перенаправляет
        return redirect('cart')

    # добавление в корзину если пользователь не авторизирован
    else:

        product_variation = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product,
                                                      variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            # получаем ИД корзины
            cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            # создаем корзину если её нет
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:

            # cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # есть характкристика продкта

            # exist_variation => database

            # текущая характеристика продукта
            # current_variation => product_variation
            # item_id => database
            ex_var_list = []  # пременная для передачи сущестующих характеристик продука
            id = []  # переменная для хранения id продукта
            # выгружаем список характеристик в ex_var_list
            for item in cart_item:
                exist_variation = item.variations.all()
                ex_var_list.append(list(exist_variation))  # передаем характеристики продукта
                id.append(item.id)  # передаем id продукта
            # print(ex_var_list)

            # проверяем есть ли продукт с такимиже характеристиками в корзине
            if product_variation in ex_var_list:
                # return HttpResponse('True')
                # увеличиваем количество продукта в корзине
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # return HttpResponse('False')
                # добавляем продукт в корзину
                # добавляем характеристик продукта в корзину
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            # добовляем продукт в корзину
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            # добавляем характеристик продукта в карзину
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        # переходим в корзину redirect-перенаправляет
        return redirect('cart')
        # return HttpResponse(cart_item.quantity)
        # exit()


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (total * 20) / 100  # ндс
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (total * 20) / 100  # ндс
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/checkout.html', context)
