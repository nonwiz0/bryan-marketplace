from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_detail_paycash, name='cart'),
    path('success/', views.success, name='success'),

    path('cart_online/', views.cart_detail_online, name='cart_online'),
]