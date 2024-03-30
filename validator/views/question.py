from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, inline_serializer

from utils.pagination import CustomPageNumberPagination

from validator.services.question import QuestionService
from validator.serializers import (
    QuestionRequest, QuestionResponse, BaseQuestion, PaginatedQuestionResponse
)


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
class QuestionGet(ViewSet):    
    """
    ViewSet to return all or specific questions.
    """

    pagination_class = CustomPageNumberPagination()
    service_class = QuestionService()
    
    @extend_schema(
        description='Request and Response data to get a question',
        responses=QuestionResponse,
    )
    def get(self, request, pk):
        question = self.service_class.get(user=request.user, pk=pk)
        serializer = QuestionResponse(question)
        
        return Response(serializer.data)
    
    @extend_schema(
        description='Returns all questions corresponding to a specified user.',
        responses=PaginatedQuestionResponse,
    )
    def get_all(self, request):
        # query param to determine time range or response
        time_range = request.query_params.get('time_range') 
        questions = self.service_class.get_all(user=request.user, time_range=time_range)
        serializer = QuestionResponse(questions, many=True)

        paginator = self.pagination_class
        page = paginator.paginate_queryset(serializer.data, request)

        return paginator.get_paginated_response(page)
    
    @extend_schema(
        description='Returns questions with mode PENGAWASAN for privileged users based on keyword and time range.',
        responses=PaginatedQuestionResponse,
    )
    def get_all_privileged(self, request):
        # query param to determine time range or response
        time_range = request.query_params.get('time_range') 
        keyword =  request.query_params.get('keyword', '')

        questions = self.service_class.search_privileged(user=request.user, time_range=time_range, keyword=keyword)
        serializer = QuestionResponse(questions, many=True)

        paginator = self.pagination_class
        page = paginator.paginate_queryset(serializer.data, request)

        return paginator.get_paginated_response(page)

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
    