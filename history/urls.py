from django.urls import path
from .views.search_bar import SearchHistory

urlpatterns = [
    path('search/', SearchHistory.as_view(), name='search_history'),
]
