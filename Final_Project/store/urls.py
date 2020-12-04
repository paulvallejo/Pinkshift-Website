from django.urls import path
from . import views

"""
In this file, we map all of the store's URLs. We import "path" form django to power our URL pattern and import views
to use the functions created in views.py.
"""

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.aboutPage, name='about'),
    path('tour/', views.tourPage, name='tour'),
    path('category/<slug:category_slug>', views.home, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.productPage, name='product_detail'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),
    path('thankyou/<int:order_id>', views.thanks_page, name='thanks_page'),
    path('search/', views.search, name='search')
]
