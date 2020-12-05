from django.db import models
from django.urls import reverse

"""
This file contains all of the models for this website. Info taken from:
https://docs.djangoproject.com/en/3.1/topics/db/models/
"""
# Category Model


class Category(models.Model):
    """
    This class is used to store product category attributes and maps it to a database column.
    """
    name = models.CharField(max_length=250, unique=True)  # The name of the product category.
    slug = models.SlugField(max_length=250, unique=True)  # The part of the URL that defines a particular page
    description = models.TextField(blank=True)            # Category description
    image = models.ImageField(upload_to='category', blank=True)  # Category image

    class Meta:
        """
        Class such that the word "category" is spelled correctly in plural
        context.
        """
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        """
        A function that accesses each product by their category URL by using Django's reverse function
        """
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        """
        This function simply returns a readable representation of a category.
        """
        return self.name


# Product Model


class Product(models.Model):
    """
    This class is used to store product attributes and maps it to a database column. The objects created from this
    class are the items you're selling.
    """
    objects = None
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Class such that the word "product" is spelled correctly in plural
        context.
        """
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        """
        A function that accesses each product by their category URL by using Django's reverse function
        """
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        """
        This function simply returns a readable representation of a product.
        """
        return self.name


# Cart Model


class Cart(models.Model):
    """
    This class allows users to pick the items they want to purchase and store it as a "cart" object. This information
    is stored until the user is ready to make a purchase.
    """
    DoesNotExist = None
    objects = None
    cart_id = models.CharField(max_length=250, blank=True)  # The "session" or cart for a particular user
    date_added = models.DateField(auto_now_add=True)        # The date a particular cart was created

    class Meta:
        """
        This class defines the database table name
        """
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        """
        This function simply returns a readable representation of a cart.
        """
        return self.cart_id


class CartItem(models.Model):
    """
    This class creates CartItem objects that includes information about a single object that's added to the cart. This
    adds another table to our database calle "CartItem".
    """
    DoesNotExist = None
    objects = None
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        """
        This class defines the database table name
        """
        db_table = 'CartItem'

    def sub_total(self):
        """
        This function calculates the total amount of the product based on its quantity and price
        """
        return self.product.price * self.quantity

    def __str__(self):
        """
        This function simply returns a readable representation of a cart item.
        """
        return self.product


# Order model


class Order(models.Model):
    """
    This class creates order objects once payment has been processed. All of the attributes refer to some descriptive
    element of an order.
    """
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCountry = models.CharField(max_length=250, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry = models.CharField(max_length=250, blank=True)

    class Meta:
        """
        This class defines the database table name
        """
        db_table = 'Order'
        ordering = ['-created']

    def __str__(self):
        """
        This function simply returns a readable representation of an order.
        """
        return str(self.id)


class OrderItem(models.Model):
    """
    This class creates order item objects for orders similar to how cart item objects are created for carts.
    """
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        """
        This class defines the database table name
        """
        db_table = 'OrderItem'

    def sub_total(self):
        """
        This function calculates the sub-total of an order item.
        """
        return self.quantity * self.price

    def __str__(self):
        """
        This function simply returns a readable representation of an order item.
        """
        return self.product
