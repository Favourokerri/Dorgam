from django.shortcuts import render, redirect
from django.conf import settings
import requests
from datetime import timedelta
from django.utils.dateparse import parse_date
from django.utils import timezone
from .models import Product, Category
from decimal import Decimal
from datetime import datetime
from django.shortcuts import get_object_or_404
from core.decorator import is_logged_in
from django.contrib import messages
from .models import Product, Cart, CartItem, State,Order, OrderItem
from django.http import JsonResponse
import json
# Create your views here.
def products(request):
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', 'all')
    
    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)
    
    if category_filter != 'all':
        products = products.filter(categories__id=category_filter)

    categories = Category.objects.all()
    context = {'products': products, 'search_query': search_query,
               'categories': categories, 'category_filter': category_filter}
    return render(request, "mainSite/shopPage.html", context)

def single_product(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(categories__in=product.categories.all()).exclude(id=product.id)
    context = {"product": product, 'products': related_products}
    return render(request, "mainSite/singleProductPage.html", context)


@is_logged_in
def cart_page(request):
    try:
        cart = Cart.objects.filter(user=request.user, completed=False).first()
        states = State.objects.filter(delivery_available=True).all()
        
        if not cart:
            cartitems = []
            total_price = 0
        else:
            cartitems = cart.cartitems.all()
            total_price = sum(item.total_price() for item in cartitems)

        max_shipping_duration_item = max(cartitems, key=lambda item: item.product.shipping_duration, default=None)
        
        if max_shipping_duration_item:
            shipping_duration_days = max_shipping_duration_item.product.shipping_duration
            delivery_date = (timezone.now() + timedelta(days=shipping_duration_days)).date()
        else:
            delivery_date = None  # No items in cart, no shipping date

        context = {
            "cart": cart,
            "cartitems": cartitems,
            "total_price": total_price,
            "states":states,
            "delivery_date": delivery_date
        }
        return render(request, "mainSite/cartPage.html", context)

    except Exception as e:
        messages.error(request, "An error occurred while loading your cart.")
        print(f"Error: {e}")
        return render(request, "mainSite/cartPage.html")


@is_logged_in
def add_to_add(request):
    if request.method == 'POST':
        try:
            quantity = request.POST['quantity']
            product_id = request.POST.get('product_id')
            product = Product.objects.filter(id=product_id).first()
            quantity = int(quantity)

            if quantity <= 0:
                quantity = 1

            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cartitem.quantity += quantity
            cartitem.save()
            messages.success(request, "item added successfully")
            return redirect('cart')
        except Exception as e:
            messages.error(request, "sorry some error occured. try again later")
            print(e)
    return render(request, "mainSite/cartPage.html")

@is_logged_in
def remove_item(request, id):
    try:
        cart = Cart.objects.filter(user=request.user, completed=False).first()
        if cart:
            cartitem = cart.cartitems.filter(id=id).first()
            if cartitem:
                cartitem.delete()
                messages.success(request, "item deleted successfully")
    except Exception as e:
        print(e)
    return redirect('cart')

@is_logged_in
def update_item(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    quantity = data['quantity']
    cart = Cart.objects.filter(user=request.user, completed=False).first()
    cart_item = CartItem.objects.filter(cart=cart, id=item_id).first()
    cart_items = cart.cartitems.all()

    if (quantity == "" or quantity == 0):
         return JsonResponse({"message":"item must be greater than zero"}, safe=False)
    try:
        quantity = int(quantity)
        cart_item.quantity = quantity
        cart_item.save()

        total_price = sum(item.total_price() for item in cart_items)
    except Exception as e:
        messages.error(request, 'sorry some error occured')
        print(e)
       
    return JsonResponse({"message":"item updated successfully", "total_price":total_price}, safe=False)

@is_logged_in
def get_shipng_fee(request):
    data = json.loads(request.body)
    state_id = data['state_id']
   
    state = State.objects.filter(id=state_id).first()
       
    return JsonResponse({"message":"fee fetched successfully", "shippingFee":state.shipping_fee}, safe=False)

@is_logged_in
def orders(request):
    orders = Order.objects.prefetch_related('order_items').filter(user=request.user, status='Completed').order_by('-created_at')
    for order in orders:
        for item in order.order_items.all():
            item.total_price_display = item.product.price * item.quantity
    return render(request, 'mainSite/ordersPage.html', {'orders': orders})

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
@is_logged_in
def check_out(request):
    try:
        if request.method == "POST":
            phone_number = request.POST.get('phone')
            address = request.POST.get('address')
            state_id = request.POST.get('state')
            shipping_fee = request.POST.get('shipping-fee')
            delivery_date = request.POST.get('deliveryDate')
                
            user = request.user
            cart = Cart.objects.filter(user=request.user, completed=False).first()
            cartitems = cart.cartitems.all()
            cart_item_amount = sum(item.total_price() for item in cartitems)
            total_amount = cart_item_amount + Decimal(shipping_fee)
            delivery_date_obj = datetime.strptime(delivery_date, '%b. %d, %Y')

            delivery_date = delivery_date_obj.date()
            state = State.objects.filter(id=state_id).first()
           

            orders = Order.objects.create(user=request.user,
                                      phone_number=phone_number,
                                      state=state,
                                      shipping_address=address,
                                      cart_item_amount=cart_item_amount,
                                      shipping_fee=shipping_fee,
                                      total_amount=total_amount,
                                      delivery_date=delivery_date,)
            
            order_items = [] 
            for cart_item in cart.cartitems.all():
                order_item = OrderItem.objects.create(
                    order=orders,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    total_price=cart_item.quantity * cart_item.product.price,
                )
                order_items.append(order_item)
    
            orders.order_items.set(order_items)

             # Create Paystack payment link
            headers = {
                'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
            }

            payload = {
                'amount': int(total_amount * 100),  # Total amount in kobo (cents)
                'email': request.user.email,  # Use the user's email address

                'currency': 'NGN',
                'reference': f"order-{orders.id}",
                'callback_url': request.build_absolute_uri(f'/store/payment-success/?order_id={orders.id}'),
                'cancel_url': request.build_absolute_uri(f'/store/payment-failed/?order_id={orders.id}'),
                'metadata': {
                    'name': request.user.get_full_name(),  # User's full name
                    'phone_number': phone_number,  # User's phone number from the form
                    }
            }

            response = requests.post('https://api.paystack.co/transaction/initialize', data=payload, headers=headers)
            print(response.status_code)

            if response.status_code == 200:
                data = response.json()
                payment_url = data['data']['authorization_url']  # The URL to redirect the user to
                return redirect(payment_url)
            else:
                order = Order.objects.get(id=orders.id)
                order.payment_status = 'Failed'
                order.save()
                return render(request, 'payment_failed.html', {'message': 'Failed to create payment session.'})

        
    except Exception as e:
        print(e)
    return render(request, "mainSite/cartPage.html")


def payment_success(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    reference = request.GET.get('reference')

    # Verify the payment with Paystack
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
    }
    verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
    response = requests.get(verify_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['data']['status'] == 'success':
            # Update order status to Paid
            order.payment_status = 'Paid'
            order.status = 'Completed'
            order.save()

            order_items = OrderItem.objects.filter(order=order).all()
            for item in order_items:
                item.payment_status = order.payment_status
                item.save()

            # Mark cart as completed
            cart = Cart.objects.filter(user=order.user, completed=False).first()
            if cart:
                cart.completed = True
                cart.save()

            return render(request, 'mainSite/payment_success.html', {'order': order})
    else:
        return render(request, 'mainSite/payment_failed.html', {'order': order})

def payment_failed(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)

    order.payment_status = 'Failed'
    order.save()

    return render(request, 'mainSite/payment_failed.html', {'order': order})


