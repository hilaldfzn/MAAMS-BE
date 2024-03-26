# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from history.serializers import HistoryResponse
from utils.pagination import CustomPageNumberPagination
from history.services.search_bar import SearchBarHistoryService
from history.enums import HistoryType

class SearchHistory(generics.ListAPIView):
    serializer_class = HistoryResponse
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mode = request.query_params.get('mode')
        keyword = request.query_params.get('keyword', '')
        
        result = SearchBarHistoryService().filter(user=request.user, keyword=keyword, mode=mode)
        serializer = HistoryResponse(result, many=True)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(serializer.data, request)
        
        return paginator.get_paginated_response(page)