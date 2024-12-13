from django.contrib import admin
from .models import Category, Product, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_categories',)
    list_filter = ('categories',)
    search_fields = ('name', 'categories__name')
    ordering = ('-created_at',)

    def get_categories(self, obj):
        """Display categories as a comma-separated list."""
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

# Register the Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed', 'get_total_items', 'get_total_price', 'created_at',)
    list_filter = ('completed', 'user')
    search_fields = ('user__username',)
    ordering = ('-created_at',)

    def get_total_items(self, obj):
        """Display the total number of items in the cart."""
        return obj.cartitems.count()  # Counting all CartItems related to this Cart
    get_total_items.short_description = 'Total Items'

    def get_total_price(self, obj):
        """Calculate and display the total price for the cart."""
        total = sum([item.total_price() for item in obj.cartitems.all()])
        return f"${total:.2f}"  # Return the total price formatted as a string
    get_total_price.short_description = 'Total Price'


# Register the CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart__user', 'product', 'quantity', 'total_price', 'created_at', 'updated_at')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__username', 'product__name')
    ordering = ('-created_at',)

    def total_price(self, obj):
        """Display the total price for this cart item."""
        return f"${obj.total_price():.2f}"
    total_price.short_description = 'Total Price'
