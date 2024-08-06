from django.urls import path
from .views import register_view, login_view, logout_view, home_view, create_room_view, join_room_view, room_view, clear_chat_view, load_messages, send_message

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('create/', create_room_view, name='create_room'),
    path('join/', join_room_view, name='join_room'),
    path('room/<str:room_name>/', room_view, name='room'),
    path('clear_chat/<str:room_name>/', clear_chat_view, name='clear_chat'),
    path('load_messages/<str:room_name>/', load_messages, name='load_messages'),
    path('send_message/<str:room_name>/', send_message, name='send_message'),
]
