from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_duration = models.IntegerField(help_text="number of days for ordered product to get to consumer")
    is_featured = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='products')
    description = CKEditor5Field(config_name='default')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
