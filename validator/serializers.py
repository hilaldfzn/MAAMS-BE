from rest_framework import serializers
from validator.models.question import Question
from authentication.serializers import CustomUserSerializer

class BaseQuestion(serializers.Serializer):
    MODE_CHOICES = Question.ModeChoices

    class Meta:
        ref_name = 'base question'
        
    mode = serializers.ChoiceField(choices=MODE_CHOICES)
    
class QuestionRequest(BaseQuestion):
    class Meta:
        ref_name = 'question request'

    question = serializers.CharField()
    
class QuestionResponse(BaseQuestion):
    class Meta:
        ref_name = 'question response'
    
    id = serializers.UUIDField()
    question = serializers.CharField()
    created_at = serializers.DateTimeField()
    

