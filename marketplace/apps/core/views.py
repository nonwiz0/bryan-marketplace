from django.shortcuts import render

from apps.product.models import Product

from apps.inbox.models import ThreadModel

# Create your views here.
def frontpage(request):
     latest_products = Product.objects.all()[0:8]

     return render(request, 'core/frontpage.html', {'latest_products': latest_products})

def contact(request):
    return render(request, 'core/contact.html')

def chat(request):
    return render(request, 'chat/index.html')

def inbox(request):
    return render(request, 'inbox/inbox.html')

