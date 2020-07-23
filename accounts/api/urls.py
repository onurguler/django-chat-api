from django.urls import path, include
from accounts.api.auth.views import Register, Login

app_name = "accounts"

auth_urls = [
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
]
