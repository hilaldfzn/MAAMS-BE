from django.db import models
import uuid

class Question(models.Model):
    class ModeChoices(models.TextChoices):
        PRIBADI = "PRIBADI", "pribadi"
        PENGAWASAN = "PENGAWASAN", "pengawasan"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # TODO:  uncomment when user already implemented
    # user = models.ForeignKey(..., on_delete=models.SET_NULL, null=True)
    question = models.CharField()
    mode = models.CharField(max_length = 20, choices=ModeChoices.choices, default=ModeChoices.PRIBADI)
    created_at = models.DateTimeField(auto_now_add=True)