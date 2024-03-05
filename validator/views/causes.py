from rest_framework.views import APIView
from rest_framework.response import Response
from validator.services.causes import CausesService
from validator.services.question import QuestionService
from validator.serializers import CausesRequest, CausesResponse
from rest_framework import status
from drf_spectacular.utils import extend_schema

class CausesPost(APIView):
    @extend_schema(
        description='Request and Response data for creating a cause',
        request=CausesRequest,
        responses=CausesResponse,
    )
    def post(self, request):
        request_serializer = CausesRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        cause = CausesService.create(user=request.user, **request_serializer.validated_data)
        response_serializer = CausesResponse(cause)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CausesGet(APIView):
    @extend_schema(
        description='Request and Response data to get a cause',
        responses=CausesResponse,
    )
    def get(self, request, pk):
        question = QuestionService.get(self, user=request.user, pk=pk)
        cause = CausesService.get(question, pk=pk)
        serializer = CausesResponse(cause)

        return Response(serializer.data)

class CausesPut(APIView):
    @extend_schema(
        description='Request and Response data for updating a cause',
        request=CausesRequest,
        responses=CausesResponse,
    )
    def put(self, request, pk):
        question = QuestionService.get(self, user=request.user, pk=pk)
        request_serializer = CausesRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        cause = CausesService.update(question, pk=pk, **request_serializer.validated_data)
        response_serializer = CausesResponse(cause)

        return Response(response_serializer.data)