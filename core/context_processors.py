from django.shortcuts import render
from .models import Contact, Service, SocialMedia
from ecommerceShop.models import Cart

# Create your views here.
def contact_info(request):
    contactInfo = Contact.objects.first()
    return {"contact": contactInfo}

def services(request):
    services = Service.objects.all()[:5]
    return {"services": services}

def social_media_view(request):
    social = SocialMedia.objects.first()  # You can adjust the query as needed
    return {'social': social}

def cart_item_count(request):
    """
    Context processor to calculate the total number of items in the cart.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user, completed=False).first()
            if cart:
                total_items = sum(item.quantity for item in cart.cartitems.all())
            else:
                total_items = 0
        except Exception as e:
            print(f"Error calculating cart item count: {e}")
            total_items = 0
    else:
        total_items = 0

    return {"cart_item_count": total_items}