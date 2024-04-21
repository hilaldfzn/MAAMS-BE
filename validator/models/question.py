from django.db import models
import uuid

from pydantic import ValidationError
from authentication.models import CustomUser
from .tag import Tag

class Question(models.Model):
    class Meta:
        app_label = 'validator'
        
    class ModeChoices(models.TextChoices):
        PRIBADI = "PRIBADI", "pribadi"
        PENGAWASAN = "PENGAWASAN", "pengawasan"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=40, default='')
    question = models.CharField()
    mode = models.CharField(max_length = 20, choices=ModeChoices.choices, default=ModeChoices.PRIBADI)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def clean(self):
        super().clean()
        if not self.tags.exists():
            raise ValidationError("Each question must have at least one tag associated with it.")