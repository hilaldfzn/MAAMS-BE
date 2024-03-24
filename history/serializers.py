from rest_framework import serializers
from validator.serializers import BaseQuestion

class HistoryResponse(BaseQuestion):
    class Meta:
        ref_name = 'QuestionResponse'
    
    id = serializers.UUIDField()
    question = serializers.CharField()
    created_at = serializers.DateTimeField()