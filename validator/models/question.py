from django.db import models
import uuid
from authentication.models import CustomUser

class Question(models.Model):
    class Meta:
        app_label = 'validator'
        
    class ModeChoices(models.TextChoices):
        PRIBADI = "PRIBADI", "pribadi"
        PENGAWASAN = "PENGAWASAN", "pengawasan"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    question = models.CharField()
    mode = models.CharField(max_length = 20, choices=ModeChoices.choices, default=ModeChoices.PRIBADI)
    created_at = models.DateTimeField(auto_now_add=True)