from rest_framework.views import APIView
from rest_framework.response import Response
from validator.serializers import QuestionRequest, QuestionResponse, BaseQuestion
from rest_framework import status

class QuestionAPI(APIView):
    def post(self, request):
        return ""
    
    def get(self, request, pk):
        return ""
    
    def put(self, request, pk):
        return ""