from django.urls import path
from validator.views.question import QuestionGet, QuestionPost, QuestionPut
from validator.views.causes import CausesGet, CausesPost, CausesPut

app_name = 'validator'

urlpatterns = [
    path('baru/', QuestionPost.as_view(), name="create_question"),
    path('<uuid:pk>/', QuestionGet.as_view(), name="get_question"),
    path('ubah/<uuid:pk>/', QuestionPut.as_view(), name="put_question"),
    path('causes/', CausesPost.as_view(), name="create_causes"),
    path('causes/<uuid:question_id>/<uuid:pk>', CausesGet.as_view(), name="get_causes"),
    path('causes/update/<uuid:question_id>/<uuid:pk>/', CausesPut.as_view(), name="put_causes"),
]
