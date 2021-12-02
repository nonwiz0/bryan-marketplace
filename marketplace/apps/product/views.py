import random 
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from apps.vendor.models import Vendor
from .models import Category, Product
from .forms import AddToCartForm
from apps.cart.cart import Cart
import hashlib

# Create your views here.
def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'product/search.html', {'products': products, 'query':query })

def send_a_message(req, buyer, seller, product):
    u_buyer = req.user.vendor
    u_seller = Vendor.objects.get(id=seller)
    pk = (u_buyer.name+u_seller.name+product).encode()
    hash_pk = hashlib.md5(pk).hexdigest()
    data = {
        'id': hash_pk,
        'buyer': u_buyer.name,
        'seller': u_seller.name,
        'product': product
    }
    if 'messages' in u_buyer.inbox:
        u_buyer.inbox['messages'].append(data)
    else:
        u_buyer.inbox['messages'] = []
        u_buyer.inbox['messages'].append(data)
    if 'messages' in u_seller.inbox:
        u_seller.inbox['messages'].append(data)
    else:
        u_seller.inbox['messages'] = []
        u_seller.inbox['messages'].append(data)
    u_seller.save()
    u_buyer.save()
    return redirect('room', room_name=hash_pk)

    return JsonResponse({"status": True})

def product(request, category_slug, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The product was added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    return render(request, 'product/product.html', {'form': form, 'product': product, 'similar_products': similar_products})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    return render(request, 'product/category.html', {'category': category})
