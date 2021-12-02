from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from .models import Vendor
from apps.product.models import Product
from .forms import ProductForm

# Create your views here.
def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')

    else:
        form = UserCreationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})

@login_required
def vendor_admin(request):
    # So this is the profile
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    inbox = ["none"]
    if "messages" in vendor.inbox:
        inbox = vendor.inbox["messages"]

    followers = vendor.followers.all()

    if len(followers) == 0:
            is_following = False

    for follower in followers:
        if follower == request.user:
                is_following = True
                break
        else:
                is_following = False

        number_of_followers = len(followers)

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders, 'inbox': inbox})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {'form': form})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        birth_date = request.POST.get('birth_date', '')
        location = request.POST.get('location','')
        profile_picture = request.POST.get('profile_picture', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.birth_date = birth_date
            vendor.location = location
            vendor.profile_picture = profile_picture
            vendor.save()

            return redirect('vendor_admin')

    return render(request, 'vendor/edit_vendor.html', {'vendor': vendor})

def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendors': vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendor/vendor.html', {'vendor': vendor})


@login_required
def confirmed_order(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/confirmed_order.html', {'vendor': vendor, 'products': products, 'orders': orders})

@login_required
def product_table(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/product_table.html', {'vendor': vendor, 'products': products, 'orders': orders})

@login_required
def add_follower(request, vendor):
    vendor = Vendor.objects.get()
    vendor.user = request.user()
    vendor.save()

    return redirect('vendor/vendor_admin', pk=vendor.pk)


@login_required
def remove_follower(self, vendor_id,):
    vendor = Vendor.objects.get(pk=vendor_id)
    vendor.followers.remove(self.request.user.vendor)

    return redirect('vendor', pk=vendor.pk)
