from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('msg-list/', views.get_all_messages, name='get_all_messages'),
    path('usr-list/', views.get_all_users, name='get_all_users'),
    path('sent-msg/', views.get_messages_by_sender_id, name='messages_by_id'),
    path('received-msg/', views.get_messages_by_receiver_id, name='messages_by_id'),
    path('usr-unread-msg', views.get_unread_messages_by_user_id, name='messages_by_id'),
    path('usr-msg-delete', views.delete_user_messages, name='delete_messages_by_id'),
    path('send-msg/', views.send_msg, name='send_message'),
    path('delete-msg/', views.delete_message, name='delete_message'),
    path('add-users/', views.add_users, name='add_users'),
    path('read-msg/', views.read_message, name='read_message'),
]