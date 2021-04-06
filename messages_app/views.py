import random
from messages_app.models import Message
from messages_app.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from messages_app.serializers import MessagesSerializer
from messages_app.serializers import UserSerializer


@api_view(['GET'])
def home_page(request):
    return Response('Hi welcome to the the messages app')


# Return all messages in database
@api_view(['GET'])
def get_all_messages(request):
    messages = Message.objects.all()
    if not messages:
        return Response("no Messages to show")
    else:
        serialized_message = MessagesSerializer(messages,many=True)
        return Response(serialized_message.data)


# Return all users in database
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    if not users:
        return Response("No users to show")
    else:
        serialized_message = UserSerializer(users,many=True)
        return Response(serialized_message.data)


# Add users with random details to database, made for test
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


# Return all messages sent by user with given ID
@api_view(['GET'])
def get_messages_by_sender_id(request):
    if 'user_id' not in request.query_params:
        return Response("Illegal URL, please pass parameters in the format: url/msg_app.sent-msg?msg_id=[your user ID]")
    try:
        user = User.objects.get(_id=request.query_params['user_id'])
    except:
        return Response("Couldn't find user with matching ID")
    messages = Message.objects.filter(sender=user)
    if not messages:
        return Response("User has no sent messages")
    serialized = MessagesSerializer(messages, many=True)
    return Response(serialized.data)


# Return all messages received by user with given ID
@api_view(['GET'])
def get_messages_by_receiver_id(request):
    if 'user_id' not in request.query_params:
        return Response("Illegal URL, please pass parameters in the format: url/msg_app.sent-msg?msg_id=[your user ID]")
    try:
        user = User.objects.get(_id=request.query_params['user_id'])
    except:
        return Response("Couldn't find user with matching ID")
    messages = Message.objects.filter(receiver=user)
    if not messages:
        return Response("User has no received messages")
    serialized = MessagesSerializer(messages, many=True)
    return Response(serialized.data)


# Get user all unread messages
@api_view(['GET'])
def get_unread_messages_by_user_id(request):
    if 'user_id' not in request.query_params:
        return Response("Illegal URL, please pass parameters in the format: url/msg_app.sent-msg?msg_id=[your user ID]")
    try:
        user = User.objects.get(_id=request.query_params['user_id'])
    except:
        return Response("Couldn't find user with matching ID")
    messages = Message.objects.filter(sender=user, read=False)
    if not messages:
        return Response('User has no unread messages')
    serialized = MessagesSerializer(messages,many=True)
    return Response(serialized.data)


# read message content by it's ID
@api_view(['GET'])
def read_message(request):
    message = Message.objects.filter(read=True, sender_id=request.query_params['user_id']).order_by('sent_time')[0]
    message.read = True
    if not message:
        return Response('No sent messages for current user')
    serialized = MessagesSerializer(message, many=False)
    return Response(serialized.data)


# delete all messages of specific user
@api_view(['GET', 'DELETE'])
def delete_user_messages(request):
    if 'user_id' not in request.query_params:
        return Response("Illegal URL, please pass parameters in the format: url/msg_app.sent-msg?msg_id=[your user ID]")
    try:
        user = User.objects.get(_id=request.query_params['user_id'])
    except:
        return Response("Couldn't find user with matching ID")
    messages = messages = Message.objects.filter(sender=user)
    messages.delete()
    return Response('All ' + user.first_name + '\'s messages successfully deleted')


# Delete message by ID
@api_view(['GET', 'DELETE'])
def delete_message(request):
    try:
        message = Message.objects.get(id=request.query_params['msg_id'])
    except:
        return Response("Illegal URL or message ID")
    message.delete()
    return Response('Successfully deleted message')


# send message from given sender to given receiver
@api_view(['GET', 'POST'])
def send_msg(request):
    message_body = request.data
    try:
        sender = User.objects.get(_id=message_body['sender_id'])
        receiver = User.objects.get(_id=message_body['receiver_id'])
    except:
        return Response("Couldn't find user with matching ID")
    new_message = Message(sender=sender, receiver=receiver, content=message_body['message'])
    new_message.save()
    return Response(sender.first_name + ' successfully sent a message to ' + receiver.first_name)
