from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(
        max_length=32,
        unique=True,
        null=False,
        blank=False,
        help_text='Required. %(username_max_length)d characters or fewer. Letters, digits and _ only.' % {
            'username_max_length': 32},
        error_messages={
            'unique': "A user with that username already exists."
        },
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @classmethod
    def create_user(cls, username, email=None, password=None, first_name=None, last_name=None):

        new_user = cls.objects.create_user(username, email=email, password=password,
                                           first_name=first_name, last_name=last_name)

        return new_user
