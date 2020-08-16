from rest_framework import serializers

from chat.models import Message, Conversation
from accounts.api.users.serializers import UserSerializer


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text',)


class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')
    to = serializers.SerializerMethodField('get_conversation')

    class Meta:
        model = Message
        fields = ('owner', 'to', 'text', 'created_at', 'updated_at', 'id')
        read_only_fields = ('owner', 'to', 'created_at', 'updated_at', 'id')

    def get_owner(self, obj):
        owner = obj.owner
        owner_serializer = UserSerializer(owner)
        return owner_serializer.data

    def get_conversation(self, obj):
        conversation = obj.to
        conversation_serializer = ConversationSerializer(conversation)
        return conversation_serializer.data


class ConversationMessageSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')

    class Meta:
        model = Message
        fields = ('id', 'owner', 'text', 'created_at', 'updated_at')
        read_only_fields = fields

    def get_owner(self, obj):
        owner = obj.owner
        owner_serializer = UserSerializer(owner)
        return owner_serializer.data


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField('get_participants')
    last_message = serializers.SerializerMethodField('get_last_message')

    class Meta:
        model = Conversation
        fields = ('uuid', 'participants', 'created_at',
                  'updated_at', 'last_message')
        read_only_fields = fields

    def get_participants(self, obj):
        participants = obj.participants
        participants_serializer = UserSerializer(participants, many=True)
        return participants_serializer.data

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-created_at')[0]
        message_serializer = ConversationMessageSerializer(last_message)
        return message_serializer.data
