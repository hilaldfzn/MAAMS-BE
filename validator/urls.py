from django.urls import path
from validator.views.question import Question

app_name = 'validator'

urlpatterns = [
    path('baru/', Question.as_view(), name="create_question"),
    path('<uuid:pk>/', Question.as_view(), name="get_question"),
    path('ubah/<uuid:pk>/', Question.as_view(), name="patch_question")
]
