from .models import Category


def menu_links(request):
    """
    *Parameters*
    request:
        An http response object

    *Return*
        dictionary
    """
    links = Category.objects.all()
    return dict(links=links)
