from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
import channels.layers
import json

from chat.api.serializers import (SendMessageSerializer, MessageSerializer,
                                  ConversationSerializer, ConversationMessageSerializer)
from chat.models import Conversation, Message


class SendMessage(APIView):
    """
    Send a message to a user
    """
    serializer_class = SendMessageSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, username):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        text = data["text"]

        User = get_user_model()

        owner = request.user
        to_user = None

        if owner.username == username:
            return Response({
                'username': 'Can not send to message yourself.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                'username': "%s not found." % username
            }, status=status.HTTP_404_NOT_FOUND)

        # get private 1-1 conversation
        conversation_qs = owner.conversations.filter(max_members=2,
                                                     participants__in=[owner, to_user])

        if not conversation_qs.exists():
            print("conversation bulunamadı")
            conversation = Conversation.objects.create()
            conversation.participants.set([owner, to_user])
            # conversation.participants.add(owner)
            # conversation.participants.add(to_user)
        else:
            conversation = conversation_qs[0]

        for participant in conversation.participants.all():
            print(participant)
        message = Message.objects.create(
            owner=owner, to=conversation, text=text)

        message_serializer = MessageSerializer(message, read_only=True)

        message_json = json.dumps(message_serializer.data)
        conversation_group_name = 'chat_%s' % conversation.uuid
        channel_layer = channels.layers.get_channel_layer()
        # Send message to room group
        async_to_sync(channel_layer.group_send)(
            conversation_group_name,
            {
                'type': 'chat_message',
                'message': message_json
            }
        )
        return Response({
            'message': message_serializer.data
        }, status=status.HTTP_201_CREATED)


class GetConversations(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        conversations = user.conversations.all()
        conversations_serializer = ConversationSerializer(
            conversations, many=True)
        return Response(conversations_serializer.data, status=status.HTTP_200_OK)


class GetUserChatMessages(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, username):
        User = get_user_model()

        user = request.user
        to_user = None

        try:
            to_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                'username': "%s not found." % username
            }, status=status.HTTP_404_NOT_FOUND)

        # get private 1-1 conversation
        conversation_qs = user.conversations.filter(max_members=2,
                                                    participants__in=[user, to_user])

        if not conversation_qs.exists():
            return Response({
                'conversation': "Conversation not found"
            }, status=status.HTTP_404_NOT_FOUND)

        conversation = conversation_qs[0]
        messages = conversation.messages.order_by('-created_at')
        messages_serializer = ConversationMessageSerializer(
            messages, many=True)

        return Response(messages_serializer.data, status=status.HTTP_200_OK)
