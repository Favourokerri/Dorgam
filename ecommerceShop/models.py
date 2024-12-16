from django.db import models
from django.contrib.auth.models import User
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


# Create your models here.
class Cart(models.Model):
    """ models for our cart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
class CartItem(models.Model):
    """ models for our cartitems """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
      """ to calculate total price of each product """
      total = self.product.price * self.quantity
      return total
   
    def __str__(self):
        return self.product.name

class State(models.Model):
    name = models.CharField(max_length=100)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)  # Reference to the order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price for this item

    DELIVERY_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    )

    delivery_status = models.CharField(
        max_length=10,
        choices=DELIVERY_STATUS_CHOICES,
        default='PENDING',  # Set the default delivery status
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending',
    )

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product.name} ({self.quantity} units)"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=300, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    shipping_address = models.TextField()
    order_items = models.ManyToManyField(OrderItem, related_name='orders')
    cart_item_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending')  # Order status
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')], default='Pending')  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"
