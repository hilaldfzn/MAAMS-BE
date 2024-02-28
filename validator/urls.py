from django.urls import path
from validator.views.questionAPI import QuestionGet, QuestionPost, QuestionPut

app_name = 'validator'

urlpatterns = [
    path('baru/', QuestionPost.as_view(), name="create_question"),
    path('<uuid:pk>/', QuestionGet.as_view(), name="get_question"),
    path('ubah/<uuid:pk>/', QuestionPut.as_view(), name="put_question")
]
