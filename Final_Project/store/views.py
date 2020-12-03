from django.shortcuts import render, get_object_or_404
from .models import Category, Product


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
# Create your views here.

def cart(request):
    return render(request, 'cart.html')
