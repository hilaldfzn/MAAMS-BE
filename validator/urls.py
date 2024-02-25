from django.urls import path
from validator.views.questionAPI import QuestionAPI

app_name = 'validator'

urlpatterns = [
    path('baru/', QuestionAPI.as_view(), name="create_question"),
    path('<uuid:pk>/', QuestionAPI.as_view(), name="get_question"),
    path('ubah/<uuid:pk>/', QuestionAPI.as_view(), name="put_question")
]
