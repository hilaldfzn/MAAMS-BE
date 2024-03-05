from rest_framework import serializers
from validator.models.question import Question
from validator.models.causes import Causes

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
    username = serializers.CharField()
class BaseCauses(serializers.Serializer):
    MODE_CHOICES = Causes.ModeChoices

    class Meta:
        ref_name = 'base causes'
        
    mode = serializers.ChoiceField(choices=MODE_CHOICES)
    
class CausesRequest(BaseCauses):
    class Meta:
        ref_name = 'causes request'

    cause = serializers.CharField()
    
class CausesResponse(BaseCauses):
    class Meta:
        ref_name = 'causes response'
    
    id = serializers.UUIDField()
    cause = serializers.CharField()