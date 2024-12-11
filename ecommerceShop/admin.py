from django.contrib import admin
from .models import Category, Product

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
