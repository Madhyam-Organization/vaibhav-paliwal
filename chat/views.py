from django.shortcuts import render
from .models import *
from .serializers import *
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import json


# class ChatAPI(APIView):
#     @staticmethod
#     def getRoomHash(sender_id, receiver_id):
#         room_name = ""
#         if str(sender_id) > str(receiver_id):
#             room_name = f"{sender_id}--{receiver_id}"
#         else:
#             room_name = f"{receiver_id}--{sender_id}"

#         room_id = hashlib.sha256(room_name.encode()).hexdigest()
#         return room_id


#     def get(self, request, receiver_id=None):
#         if receiver_id:
#             sender_id = Profile.objects.get(user=request.user).unique_id
#             room_id = self.getRoomHash(sender_id, receiver_id)

#             if not ChatRoom.objects.filter(room_id=room_id).exists():
#                 ChatRoom.objects.create(room_id=room_id)

#             chatroom = ChatRoom.objects.get(room_id=room_id)
#             chat_messages = ChatMessage.objects.filter(room=chatroom)
#             receiver_obj = Profile.objects.get(unique_id=receiver_id)
#             friends = Profile.objects.exclude(user=request.user)

#             room_serializer = ChatRoomSerializer(chatroom)
#             messages_serializer = ChatMessageSerializer(chat_messages, many=True)
#             friend_serializer = ProfileSerializer(friends, many=True)
#             receiver_profile_serializer = ProfileSerializer(receiver_obj)

#             params = {
#                 'room': room_serializer.data,
#                 'friends': friend_serializer.data,
#                 'receiver':receiver_profile_serializer.data,
#                 'messages': messages_serializer.data,
#             }
#             return Response(params)

#         friends = Profile.objects.exclude(user=request.user)
#         serializer = ProfileSerializer(friends, many=True)
#         return Response(serializer.data)


#     # The message which we write in Form should be submitted to our Consumer
#     # Consumer will save chats and will display chat on frontend in real time
#     def post(self, request):
#         pass

@login_required
def index(request):
    friends = Profile.objects.exclude(user=request.user)
    params = {
        'friends': friends,
    }
    return render(request, "index.html", params)


def getRoomHash(sender_id, receiver_id):
    room_name = ""
    if str(sender_id) > str(receiver_id):
        room_name = f"{sender_id}--{receiver_id}"
    else:
        room_name = f"{receiver_id}--{sender_id}"

    room_id = hashlib.sha256(room_name.encode()).hexdigest()
    return room_id


@login_required
def directMessage(request, receiver_id):
    sender = Profile.objects.get(user=request.user)
    room_id = getRoomHash(sender.unique_id, receiver_id)

    if not ChatRoom.objects.filter(room_id=room_id).exists():
        ChatRoom.objects.create(room_id=room_id)

    chatroom = ChatRoom.objects.get(room_id=room_id)
    messages = ChatMessage.objects.filter(room=chatroom)

    friends = Profile.objects.exclude(user=request.user)
    user_groups = SocialGroup.objects.filter(members=sender)

    receiver = Profile.objects.get(unique_id=receiver_id)

    params = {
        'friends': friends,
        'user_groups': user_groups,
        'room_id': chatroom.room_id,
        'messages': messages,
        'is_direct_message': True,
        'receiver': receiver
    }

    return render(request, 'index.html', params)


@login_required
def createGroup(request):
    if request.method == "POST":
        admin = Profile.objects.get(user=request.user)
        group_name = request.POST['group_name']

        group_id = hashlib.sha256(group_name.encode()).hexdigest()

        if not SocialGroup.objects.filter(name=group_name).exists():
            group = SocialGroup(group_id=group_id, admin=admin, name=group_name)
            group.save()
            group.members.add(admin)
            group.save()
    return render(request, 'createGroup.html')


@login_required
def groupMessage(request, group_id):
    group = SocialGroup.objects.get(group_id=group_id)
    group_messages = GroupMessage.objects.filter(group=group)

    message = group_messages[0]

    friends = Profile.objects.exclude(user=request.user)

    sender = Profile.objects.get(user=request.user)
    user_groups = SocialGroup.objects.filter(members=sender)

    params = {
        'friends': friends,
        'user_groups': user_groups,
        'group_details': group,
        'group_messages': group_messages,
        'is_direct_message': False,
    }

    return render(request, 'index.html', params)