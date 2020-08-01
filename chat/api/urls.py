from django.urls import path, include

from chat.api.views import SendMessage, GetConversations

app_name = 'chat'

user_urls = [
    path('<str:username>/send/', SendMessage.as_view(),
         name='send_message_to_user')
]

conversations_urls = [
    path('', GetConversations.as_view(), name='conversations_list')
]

urlpatterns = [
    path('user/', include(user_urls)),
    path('conversations/', include(conversations_urls))
]
