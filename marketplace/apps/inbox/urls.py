from django.urls import path
from .views import ListThreads, CreateThread, ThreadView, CreateMessage
from . import views



urlpatterns = [
    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:vendor_id>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:vendor_id>/create-message/', CreateMessage.as_view(), name='create-message')
]
