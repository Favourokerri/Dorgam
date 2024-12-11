from django.shortcuts import render
from .models import Product, Category
from django.shortcuts import get_object_or_404

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