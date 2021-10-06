from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('become_vendor/', views.become_vendor, name='become_vendor'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_vendor/', views.edit_vendor, name='edit_vendor'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='vendor/login.html'), name='login'),
    path('', views.vendors, name='vendor'),
    path('<int:vendor_id>/', views.vendor, name='vendor'),

    path('vendor_admin/confirmed_order', views.confirmed_order, name='confirmed_order'),
    path('vendor_admin/product_table', views.product_table, name='product_table'),

    path('vendor_admin/<int:vendor_id>/followers/add', views.add_follower, name='add_follower'),
    path('vendor_admin/<int:vendor_id>/followers/remove', views.remove_follower, name='remove_follower'),

]