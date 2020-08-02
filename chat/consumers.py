import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from accounts.models import User
from .models import Conversation


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.to_user_username = self.scope['url_route']['kwargs']['username']
        self.conversation_group_name = 'chat'

        if not self.user.is_authenticated:
            self.close()
            return

        if self.user.username == self.to_user_username:
            self.close()
            return

        try:
            to_user = User.objects.get(username=self.to_user_username)

            conversation_qs = self.user.conversations.filter(
                max_members=2, participants__in=[self.user, to_user])

            if not conversation_qs.exists():
                self.close()
                return

            conversation = conversation_qs[0]

            self.conversation_group_name = 'chat_%s' % conversation.uuid

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_group_name,
                self.channel_name
            )

            self.accept()
        except:
            print('hata')
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.conversation_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
