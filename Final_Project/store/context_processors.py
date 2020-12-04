from .models import Category, Cart, CartItem
from .views import _cart_id


def counter(request):
    """
    A function that's used to retrieve and display the item count
    """
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)


def menu_links(request):
    """
    A function that returns all categories from the database and names it "links" so that we can use it in the
    home page
    *Parameters*
    request:
        An http response object

    *Return*
        dictionary
    """
    links = Category.objects.all()
    return dict(links=links)
