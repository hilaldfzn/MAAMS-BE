from rest_framework.views import APIView
from rest_framework.response import Response
from validator.services.question import QuestionService
from validator.serializers import QuestionRequest, QuestionResponse, BaseQuestion
from rest_framework import status
from drf_spectacular.utils import extend_schema


class QuestionPost(APIView):
    @extend_schema(
    description='Request and Response data for creating a question',
    request=QuestionRequest,
    responses=QuestionResponse,
    )
    def post(self, request):
        request_serializer = QuestionRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        question = QuestionService.create(user=request.user, **request_serializer.validated_data)
        response_serializer = QuestionResponse(question)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
class QuestionGet(APIView):    
    @extend_schema(
        description='Request data to get a question',
        responses=QuestionResponse,
    )
    def get(self, request, pk):
        question = QuestionService.get(user=request.user, pk=pk)
        serializer = QuestionResponse(question)
        
        return Response(serializer.data)
    
class QuestionPut(APIView):
    @extend_schema(
        description='Request and Response data for updating a question',
        request=BaseQuestion,
        responses=QuestionResponse,
    )
    def put(self, request, pk):
        request_serializer = BaseQuestion(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        question = QuestionService.update_mode(user=request.user, pk=pk, **request_serializer.validated_data)
        response_serializer = QuestionResponse(question)
        
        return Response(response_serializer.data)