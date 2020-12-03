from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings

# Create your views here.


def home(request, category_slug=None):
    """
    This function combines a given template with a response object of certain rendered text.

    **Parameters**
        request:
            A template
        category_slug:
            The slug for a particular product

    **Return**
        Combination of the request object and template
    """
    category_page = None
    products = None
    if category_slug is not None:
        category_page = get_object_or_404(Category, slug=category_slug)
        # Find all products that belong to the category called to display on the page
        products = Product.objects.filter(category=category_page, available=True)
    else:
        # If there isn't a category slug, all products from home page will be displayed
        products = Product.objects.all().filter(availlable=True)
    return render(request, 'home.html', {'category': category_page, 'products': products})


def productPage(request, category_slug, product_slug):
    """
    This function combines a given template with a response object of certain rendered text.

    **Parameters**
        request:
            A template

    **Return**
        Combination of the request object and template
    """
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'product.html', {'product': product})


def _cart_id(request):
    """
    This function stores the products the user selects and keeps track of it during their session.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Pinkshift - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter,
                                             data_key=data_key, stripe_total=stripe_total, description=description))


def cart_remove(request, product_id):
    """
    This function allows the user to decrease the quantity of a product at check out.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')


def cart_remove_product(request, product_id):
    """
    This function allows the user to decrease the quantity of a product at check out.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')
