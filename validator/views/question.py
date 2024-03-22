from rest_framework.views import APIView
from rest_framework.response import Response
from validator.services.question import QuestionService
from validator.serializers import QuestionRequest, QuestionResponse, BaseQuestion
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
class QuestionPost(APIView):
    @extend_schema(
    description='Request and Response data for creating a question',
    request=QuestionRequest,
    responses=QuestionResponse,
    )
    def post(self, request):
        request_serializer = QuestionRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        question = QuestionService.create(self, user=request.user, **request_serializer.validated_data)
        response_serializer = QuestionResponse(question)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
@permission_classes([IsAuthenticated])
class QuestionGet(APIView):    
    @extend_schema(
        description='Request and Response data to get a question',
        responses=QuestionResponse,
    )
    def get(self, request, pk):
        question = QuestionService.get(self, user=request.user, pk=pk)
        serializer = QuestionResponse(question)
        
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class QuestionPut(APIView):
    @extend_schema(
        description='Request and Response data for updating a question',
        request=BaseQuestion,
        responses=QuestionResponse,
    )
    def put(self, request, pk):
        request_serializer = BaseQuestion(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        question = QuestionService.update_mode(self, user=request.user, pk=pk, **request_serializer.validated_data)
        response_serializer = QuestionResponse(question)
        
        return Response(response_serializer.data)
    
@permission_classes([IsAuthenticated])
class QuestionDelete(APIView):
    @extend_schema(
        description='Request and Response data for deleting a question',
    )
    def delete(self, request, pk):
        question = QuestionService.delete(self, user=request.user, pk=pk)
        response_serializer = QuestionResponse(question)
        
        response_data = {
            'message': 'Analisis berhasil dihapus',
            'deleted_question': response_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    