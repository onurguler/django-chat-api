from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.api.serializers import SendMessageSerializer, MessageSerializer
from chat.models import Conversation, Message


class SendMessage(APIView):
    """
    Send a message to a user
    """
    serializer_class = SendMessageSerializer
    permission_classes = (IsAuthenticated,)

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
        conversation_qs = owner.conversations.filter(
            participants__in=[to_user], max_members=2)

        if not conversation_qs.exists():
            conversation = Conversation.objects.create()
            conversation.participants.add(owner)
            conversation.participants.add(to_user)
        else:
            conversation = conversation_qs[0]

        message = Message.objects.create(
            owner=owner, to=conversation, text=text)

        message_serializer = MessageSerializer(message, read_only=True)

        return Response({
            'message': message_serializer.data
        }, status=status.HTTP_201_CREATED)
