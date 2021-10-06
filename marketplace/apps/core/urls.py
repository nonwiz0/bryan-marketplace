from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'), 

    path('chat/', views.chat, name='chat'),

    path('inbox/', views.inbox, name='inbox'),
]