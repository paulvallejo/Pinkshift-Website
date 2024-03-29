from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings

"""
In this file, we determine what content is displayed on a given page.
"""
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
        products = Product.objects.all().filter(available=True)
    return render(request, 'home.html', {'category': category_page, 'products': products})


def aboutPage(request):
    """
       This function combines a given template with a response object of certain rendered text for the
       about page.

       **Parameters**
           request:
               A template

       **Return**
           Combination of the request object and template
       """
    return render(request, 'about.html')


def tourPage(request):
    """
       This function combines a given template with a response object of certain rendered text for the page
       that lists future show dates.

       **Parameters**
           request:
               A template

       **Return**
           Combination of the request object and template
       """
    return render(request, 'tour.html')


def mediaPage(request):
    """
       This function combines a given template with a response object of certain rendered text for the page that
       will contain links to streaming services.

       **Parameters**
           request:
               A template

       **Return**
           Combination of the request object and template
       """
    return render(request, 'media.html')


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
        cart = request.session.create()  # This creates a new cart "session" if you don't have any items in your cart
    return cart


def add_cart(request, product_id):
    """
    This function calls of the information of a cart the user made and adds/concatenates a new cart item. If there
    isn't a cart made (it's the first time a user enters the site), the function creates a new cart session and
    saves it until the user checks out/pays.
    """
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:  # If there is no cart, we create a new one
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:  # Here we attempt to get cart item information
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:  # If the cart item doesn't exist, we create a new one for the session
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    """
    This function retrieves all cart items from the current session. It then calculates the total price of all of
    items in the cart. The total input is the price of all items in the cart and the counter variable is the number
    of items in the cart.
    """
    try:  # First thing is we attempt to get cart information if it's already created
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
    if request.method == 'POST':
        # print(request.POST)
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )
            # Creating the order
            try:
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )
                order_details.save()
                for order_item in cart_items:
                    or_item = OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )
                    or_item.save()

                    # Reduce the stock automatically
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()

                    # Print some kind of confirmation message when an order is created
                    print('Order created')
                return redirect('thanks_page', order_details.id)  # Home page doesn't work yet
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return False, e

    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key,
                                             stripe_total=stripe_total, description=description))


def cart_remove(request, product_id):
    """
    This function allows the user to decrease the quantity of a product at check out.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')


def cart_remove_product(request, product_id):
    """
    This function allows the user to completely remove a product from their cart.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')


def thanks_page(request, order_id):
    """
    This function takes in an order_id as an argument and uses it to find a specific order id and then returns
    an HTML template that says "thanks for your order"
    """
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'thankyou.html', {'customer_order': customer_order})


def search(request):
    """
    This function adds functionality to the search bar by directing the input text to the proper url
    """
    products = Product.objects.filter(name__contains=request.GET['title'])
    return render(request, 'home.html', {'products': products})
