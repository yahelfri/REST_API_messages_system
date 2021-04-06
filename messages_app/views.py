import random

from django.shortcuts import render
from django.http import HttpResponse
from messages_app.models import Message
from messages_app.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from messages_app.serializers import MessagesSerializer
from messages_app.serializers import UserSerializer


def index(request):
    return HttpResponse("Hi there, you are in my messages app")


@api_view(['GET'])
def get_all_messages(request):
    messages = Message.objects.all()
    serialized_message = MessagesSerializer(messages,many=True)
    return Response(serialized_message.data)

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serialized_message = UserSerializer(users,many=True)
    return Response(serialized_message.data)


@api_view(['GET', 'POST'])
def add_users(request):
    first_names_list = ["yahel", "paz", "yossi", "shimon", "guy", "dan"]
    last_names_list = ["levi", "cohen", "menashe", "aharon", "friedman", "moshe"]
    for i in range(20):
        fn = first_name=random.choice(first_names_list)
        ln = last_name=random.choice(last_names_list)
        print(fn + " - " + ln)
        nu = User(first_name=fn, last_name=ln)
        nu.save()
    return Response('successfully added users')


@api_view(['GET'])
def home_page(request):
    return Response('Hi welcome to the the messages app')


@api_view(['GET'])
def get_messages_by_user_id(request):
    print(request.query_params)
    user_id = request.query_params['user_id']
    user = User.objects.get(_id=user_id)
    messages = Message.objects.filter(sender=user)
    serialized = MessagesSerializer(messages,many=True)
    return Response(serialized.data)


@api_view(['GET'])
def get_unread_messages_by_user_id(request):
    user = User.objects.get(_id=request.query_params['user_id'])
    messages = Message.objects.filter(sender=user, read=False)
    serialized = MessagesSerializer(messages,many=True)
    return Response(serialized.data)


@api_view(['GET'])
def read_message_as_sender(request):
    message=None
    user = User.objects.get(_id=request.query_params['user_id'])
    messages = Message.objects.filter(read=False, sender_id=request.query_params['user_id'])
    if len(messages) > 0:  # return unread message
        message = messages.order_by('sent_time')[0]
        message.read = True
    else:  # no unread messages - return the last sent message
        messages = Message.objects.filter(read=True, sender_id=request.query_params['user_id'])
        if len(messages) == 0:
            return Response('No sent messages for current user')
        message = messages.order_by('sent_time')[0]
    serialized = MessagesSerializer(message, many=False)
    return Response(serialized.data)


@api_view(['GET', 'DELETE'])
def delete_user_messages(request):
    user = User.objects.get(_id=request.query_params['user_id'])
    messages = messages = Message.objects.filter(sender=user)
    messages.delete()
    return Response('All ' + user.first_name + '\'s messages successfully deleted')


@api_view(['GET', 'DELETE'])
def delete_message(request):
    message = Message.objects.get(id=request.query_params['msg_id'])
    message.delete()
    return Response('Successfully deleted message')


@api_view(['GET', 'POST'])
def send_msg(request):
    message_body = request.data
    sender = User.objects.get(_id=message_body['sender_id'])
    receiver = User.objects.get(_id=message_body['receiver_id'])
    new_message = Message(sender=sender, receiver=receiver, content=message_body['message'])
    new_message.save()
    return Response(sender.first_name + ' successfully sent a message to ' + receiver.first_name)
