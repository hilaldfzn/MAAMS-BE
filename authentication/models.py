import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    def __str__(self):
        return f'User {self.username} with UUID {self.uuid}'

    def __repr__(self):
        return f'User {self.username} with UUID {self.uuid}'