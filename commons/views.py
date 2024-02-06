from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from commons.models.dummy import DummyItem
from commons.serializers import DummyItemSerializer

class GetDummyItemAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        dummy_items = DummyItem.objects.all()
        serializer = DummyItemSerializer(dummy_items, many = True)
        return Response(serializer.data)