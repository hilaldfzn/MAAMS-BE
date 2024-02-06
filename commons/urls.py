from django.urls import path
from commons.views import GetDummyItemAPI

urlpatterns = [
    path('', GetDummyItemAPI.as_view(), name='get-dummy-item'),
]