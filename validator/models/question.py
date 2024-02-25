from django.db import models
import uuid

class Question(models.Model):
    MODE_CHOICES = [
        ('pribadi', 'Pribadi'),
        ('pengawasan', 'Pengawasan')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # TODO:  uncomment when user already implemented
    # user = models.ForeignKey(..., on_delete=models.SET_NULL, null=True)
    question = models.CharField()
    mode = models.CharField(max_length = 20, choices=MODE_CHOICES, default='pribadi')
    created_at = models.DateTimeField(auto_now_add=True)