from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('products', views.products, name="products"),
   path('product/<int:id>/', views.single_product, name="product"),
   path('cart', views.cart_page, name="cart"),
   path('addToCart', views.add_to_add, name="addToCart"),
   path('removeItem/<int:id>/', views.remove_item, name="deleteItem"),
   path('updateItem', views.update_item, name="updateItem"),
   path('shippingFee', views.get_shipng_fee, name="shippingFee"),
   path('orders', views.orders, name="orders"),
   path('checkout', views.check_out, name="checkout"),
   path('payment-success/', views.payment_success, name='payment_success'),
   path('payment-failed/', views.payment_failed, name='payment_failed'),
]
