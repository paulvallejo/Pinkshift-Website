from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    """
    This class creates a way for the admin interface to view categories in a more organized way.
    """
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    """
    This class creates a way for the admin interface to view products in a more organized way.
    """
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_pre_page = 20


admin.site.register(Product, ProductAdmin)


class OrderItemAdmin(admin.TabularInline):
    """
    This class creates a way for the admin interface to view order items in a more organized way.
    """
    model = OrderItem
    fieldsets = [
        ('Product', {'fields': ['product'], }),
        ('Quantity', {'fields': ['quantity'], }),
        ('Price', {'fields': ['price'], }),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    This class creates a way for the admin interface to view orders in a more organized way.
    """
    list_display = ['id', 'billingName', 'emailAddress', 'created']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'emailAddress']
    readonly_fields = ['id', 'token', 'total', 'emailAddress', 'created',
                       'billingName', 'billingAddress1', 'billingCity', 'billingPostcode',
                       'billingCountry', 'shippingName', 'shippingAddress1', 'shippingCity',
                       'shippingPostcode', 'shippingCountry']

    fieldsets = [
        ('ORDER INFORMATION', {'fields': ['id', 'token', 'total', 'created']}),
        ('BILLING INFORMATION', {'fields': ['billingName', 'billingAddress1',
                                            'billingCity', 'billingPostcode', 'billingCountry', 'emailAddress']}),
        ('SHIPPING INFORMATION', {'fields': ['shippingName', 'shippingAddress1',
                                             'shippingCity', 'shippingPostcode', 'shippingCountry']}),
    ]

    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        """
        This function disables the ability to delete an order on the admin side.
        """
        return False

    def has_add_permission(self, request):
        """
        This function disables the ability to add an order on the admin side.
        """
        return False
