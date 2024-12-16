import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartItem, Order

# Set your Stripe secret key here
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_view(request):
    if request.method == 'POST':
        # Get the cart and user
        cart = Cart.objects.get(user=request.user, completed=False)
        
        # Create an order
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            shipping_address=request.POST.get('shipping_address'),
            state=request.POST.get('state'),
        )

        # Create a Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),  # Amount in cents
                    },
                    'quantity': item.quantity,
                } for item in cart.cartitems.all()
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/payment-success/') + f"?order_id={order.id}",
            cancel_url=request.build_absolute_uri('/payment-failed/') + f"?order_id={order.id}",
        )

        # Redirect to Stripe Checkout
        return JsonResponse({'id': session.id})

    return render(request, 'checkout.html')

def payment_success(request):
    # Handle successful payment
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    
    # Update order status to Paid
    order.payment_status = 'Paid'
    order.status = 'Completed'
    order.save()

    # Mark cart as completed
    cart = order.cart
    cart.completed = True
    cart.save()

    return render(request, 'payment_success.html', {'order': order})

def payment_failed(request):
    # Handle failed payment
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    order.payment_status = 'Failed'
    order.save()
    return render(request, 'payment_failed.html', {'order': order})
