from rest_framework.views import APIView
from rest_framework.response import Response
from validator.services.causes import CausesService
from validator.services.question import QuestionService
from validator.serializers import CausesRequest, CausesResponse, BaseCauses
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
        cause = CausesService.create(self=CausesService, **request_serializer.validated_data)
        response_serializer = CausesResponse(cause)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CausesGet(APIView):
    @extend_schema(
        description='Request and Response data to get a cause',
        responses=CausesResponse,
    )
    def get(self, request, question_id, pk):
        cause = CausesService.get(self=CausesService, question_id=question_id, pk=pk)
        serializer = CausesResponse(cause)

        return Response(serializer.data)

class CausesPut(APIView):
    @extend_schema(
        description='Request and Response data for updating a cause',
        request=BaseCauses,
        responses=CausesResponse,
    )
    def put(self, request, question_id, pk):
        request_serializer = BaseCauses(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        cause = CausesService.update(self=CausesService, user=request.user, question_id=question_id, pk=pk, **request_serializer.validated_data)
        response_serializer = CausesResponse(cause)

        return Response(response_serializer.data)

class ValidateView(APIView):
    @extend_schema(
        description='Run Root Cause Analysis for a specific question and row',
        responses=CausesResponse,
    )
    def post(self, request, question_id):
        updated_causes = CausesService.validate(self=CausesService, question_id=question_id)
        serializer = CausesResponse(updated_causes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)