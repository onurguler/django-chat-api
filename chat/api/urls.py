from django.urls import path, include

from chat.api.views import SendMessage

app_name = 'chat'

user_urls = [
    path('<str:username>/send/', SendMessage.as_view(),
         name='send_message_to_user')
]

urlpatterns = [
    path('user/', include(user_urls)),
]
