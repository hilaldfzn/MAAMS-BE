from rest_framework import serializers
from validator.models.question import Question

class QuestionRequest(serializers.Serializer):
    MODE_CHOICES = Question.MODE_CHOICES

    class Meta:
        ref_name = 'question request'
    
    # TODO: Add user to the field
    question = serializers.CharField()
    mode = serializers.ChoiceField(choices=MODE_CHOICES)
    
class QuestionResponse(serializers.Serializer):
    class Meta:
        ref_name = 'question response'
    
    # TODO: Add user to the field
    id = serializers.UUIDField()
    question = serializers.CharField()
    mode = serializers.CharField()
    created_at = serializers.DateTimeField()
    
class QuestionUpdateModeRequest(serializers.Serializer):
    MODE_CHOICES = Question.MODE_CHOICES

    class Meta:
        ref_name = 'question update request'
    
    # TODO: Add user to the field
    id = serializers.UUIDField()
    mode = serializers.ChoiceField(choices=MODE_CHOICES)
