from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Room, Message
from .forms import RoomForm, MessageForm
from django.utils import timezone
import pytz


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'chat/home.html')

@login_required
def create_room_view(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            if room.is_private:
                room.allowed_users.set(form.cleaned_data['allowed_users'])
            room.save()
            return redirect('room', room_name=room.name)
    else:
        form = RoomForm()
    users = User.objects.all().values('id', 'username')
    return render(request, 'chat/create_room.html', {'form': form, 'users': list(users)})

@login_required
def join_room_view(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        try:
            room = Room.objects.get(name=room_name)
            if room.is_private and request.user not in room.allowed_users.all() and request.user != room.creator:
                return render(request, 'chat/join_room.html', {'error': 'You are not allowed to join this room'})
            return redirect('room', room_name=room.name)
        except Room.DoesNotExist:
            return render(request, 'chat/join_room.html', {'error': 'Room does not exist'})
    return render(request, 'chat/join_room.html')

@login_required
def room_view(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if room.is_private and request.user not in room.allowed_users.all() and request.user != room.creator:
        return redirect('home')
    form = MessageForm()
    return render(request, 'chat/room.html', {'room': room, 'form': form})

@login_required
def clear_chat_view(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.user == room.creator:
        room.messages.all().delete()
    return redirect('room', room_name=room.name)


@login_required
def load_messages(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    messages = room.messages.all().order_by('-timestamp')[:50]  # Adjust as necessary
    messages_data = []
    ist = pytz.timezone('Asia/Kolkata')
    for message in messages:
        local_timestamp = message.timestamp.astimezone(ist)
        formatted_timestamp = local_timestamp.strftime('%m-%d-%Y %H:%M')
        messages_data.append({
            'username': message.user.username,
            'content': message.content,
            'timestamp': formatted_timestamp,
            'image': message.image.url if message.image else ''
        })
    return JsonResponse({'messages': messages_data})

@login_required
def send_message(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.user = request.user
            message.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'errors': form.errors})
