from rest_framework import serializers

from chat.models import Message, Conversation
from accounts.api.users.serializers import UserSerializer


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text',)


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField('get_participants')

    class Meta:
        model = Conversation
        fields = ('uuid', 'participants', 'created_at', 'updated_at')
        read_only_fields = fields

    def get_participants(self, obj):
        participants = obj.participants
        participants_serializer = UserSerializer(participants, many=True)
        return participants_serializer.data


class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')
    to = serializers.SerializerMethodField('get_conversation')

    class Meta:
        model = Message
        fields = ('owner', 'to', 'text', 'created_at', 'updated_at')
        read_only_fields = ('owner', 'to', 'created_at', 'updated_at')

    def get_owner(self, obj):
        owner = obj.owner
        owner_serializer = UserSerializer(owner)
        return owner_serializer.data

    def get_conversation(self, obj):
        conversation = obj.to
        conversation_serializer = ConversationSerializer(conversation)
        return conversation_serializer.data
