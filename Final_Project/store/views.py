from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """
    This function combines a given template with a response object of certain rendered text.

    **Parameters**
        request:
            A template

    **Return**
        Combination of the request object and template
    """
    return render(request, 'home.html')


def productPage(request):
    """
    This function combines a given template with a response object of certain rendered text.

    **Parameters**
        request:
            A template

    **Return**
        Combination of the request object and template
    """
    return render(request, 'product.html')
# Create your views here.
