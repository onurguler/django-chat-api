from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators

from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password")

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        print(password)
        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterSerializer, self).validate(data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32,
                                     allow_blank=False)
    password = serializers.CharField()
