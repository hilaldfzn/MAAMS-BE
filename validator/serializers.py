from rest_framework import serializers
from validator.models.question import Question
from validator.models.causes import Causes

class BaseQuestion(serializers.Serializer):
    MODE_CHOICES = Question.ModeChoices

    class Meta:
        ref_name = 'BaseQuestion'
        
    mode = serializers.ChoiceField(choices=MODE_CHOICES)
    
class QuestionRequest(BaseQuestion):
    class Meta:
        ref_name = 'QuestionRequest'

    question = serializers.CharField()
    
class QuestionResponse(BaseQuestion):
    class Meta:
        ref_name = 'QuestionResponse'
    
    id = serializers.UUIDField()
    question = serializers.CharField()
    created_at = serializers.DateTimeField()
    username = serializers.CharField()
class BaseCauses(serializers.Serializer):
    MODE_CHOICES = Causes.ModeChoices

    class Meta:
        ref_name = 'BaseCauses'
        
    cause = serializers.CharField()
    
class CausesRequest(BaseCauses):
    class Meta:
        ref_name = 'CausesRequest'

    MODE_CHOICES = Causes.ModeChoices

    question_id = serializers.UUIDField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()
    mode = serializers.ChoiceField(choices=MODE_CHOICES)
class CausesResponse(BaseCauses):
    class Meta:
        ref_name = 'CausesResponse'
    
    id = serializers.UUIDField()
    question_id = serializers.UUIDField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()
    status = serializers.BooleanField()