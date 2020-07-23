from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction

from accounts.api.auth.serializers import RegisterSerializer, LoginSerializer


class Register(APIView):
    """
    User registration api view
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        User = get_user_model()

        with transaction.atomic():
            new_user = User.create_user(username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)

        token, _ = Token.objects.get_or_create(user=new_user)
        return Response({
            "token": token.key,
            "username": new_user.username
        }, status=status.HTTP_201_CREATED)


class Login(APIView):
    """
    User login api view
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        username = data["username"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed()
