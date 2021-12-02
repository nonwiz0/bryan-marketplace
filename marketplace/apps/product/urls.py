from django.urls import path

from . import views 

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('<slug:category_slug>/', views.category, name='category'),
    path('send_message/<str:buyer>/<str:seller>/<str:product>/', views.send_a_message, name="send_message")
]
