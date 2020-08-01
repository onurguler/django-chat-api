from django.urls import path, include
from accounts.api.auth.views import Register, Login, LoadUser

app_name = "accounts"

auth_urls = [
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('', LoadUser.as_view(), name='get_authenticated_user')
]

urlpatterns = [
    path('auth/', include(auth_urls)),
]
