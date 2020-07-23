from django.db import models
from django.conf import settings
import uuid


class Conversation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="conversations")
    max_members = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%(created_at)s" % {
            'created_at': self.created_at
        }


class Message(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    to = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%(owner)s at %(to)s on %(created_at)s" % {
            'owner': self.owner.username,
            'to': self.to,
            'created_at': self.created_at,
        }
