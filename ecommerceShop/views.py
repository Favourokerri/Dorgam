from django.shortcuts import render, redirect
from .models import Product, Category
from django.shortcuts import get_object_or_404
from core.decorator import is_logged_in
from django.contrib import messages
from .models import Product, Cart, CartItem
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
    context = {"product": product}
    return render(request, "mainSite/singleProductPage.html", context)

from django.contrib.auth.decorators import login_required

@is_logged_in
def cart_page(request):
    try:
        cart = Cart.objects.filter(user=request.user, completed=False).first()
        
        if not cart:
            cartitems = []
            total_price = 0
        else:
            cartitems = cart.cartitems.all()
            total_price = sum(item.total_price() for item in cartitems)

        context = {
            "cart": cart,
            "cartitems": cartitems,
            "total_price": total_price,
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

            if quantity == 0:
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

def update_item(request):
    data = json.loads(request.body)
    action = data['item_id']

   
       
    return JsonResponse("item updated successfully", safe=False)
     

