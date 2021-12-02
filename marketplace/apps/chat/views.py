from apps.chat.models import ChatRoom
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, ChatRoom
from django.contrib import messages
# Create your views here.

class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/index.html')

class Room(LoginRequiredMixin, View):
    def get(self, request, room_name):
        room = ChatRoom.objects.filter(name=room_name).first()
        chats = []

        if room:
            chats = Chat.objects.filter(room=room)
        else: 
            room = ChatRoom(name=room_name)
            room.save()
        all_inbox = request.user.vendor.inbox
        if "messages" in all_inbox:
            all_room = [item["id"] for item in all_inbox["messages"]]
            if not room_name in all_room:
                print("This user is not authorize")
                messages.add_message(request, messages.INFO, "You are not authorize to this chat")
                return redirect('frontpage')
            else :
                print("authorized")
            
        print("chat room is running", room_name)
        return render(request, 'chat/room.html', {'room_name': room_name, 'chats': chats})
