from .models import *
from rest_framework.serializers import ModelSerializer


class ProfileSerializer(ModelSerializer):
    class Meta:
        model=Profile
        fields = "__all__"


class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model=ChatRoom
        fields = "__all__"


class ChatMessageSerializer(ModelSerializer):
    class Meta:
        model=ChatMessage
        fields = "__all__"


class ChatNotificationSerializer(ModelSerializer):
    class Meta:
        model=ChatNotification
        fields = "__all__"