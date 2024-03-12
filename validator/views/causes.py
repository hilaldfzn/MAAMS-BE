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
        cause = CausesService.create(user=request.user, **request_serializer.validated_data)
        response_serializer = CausesResponse(cause)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CausesGet(APIView):
    @extend_schema(
        description='Request and Response data to get a cause',
        responses=CausesResponse,
    )
    def get(self, request, question_id, pk):
        cause = CausesService.get(user = request.user, question_id=question_id, pk=pk)
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
        cause = CausesService.update(user = request.user, question_id=question_id, pk=pk, **request_serializer.validated_data)
        response_serializer = CausesResponse(cause)

        return Response(response_serializer.data)