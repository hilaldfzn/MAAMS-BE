from django.urls import path

from validator.views.question import (
    QuestionGet, QuestionPost, QuestionPut, QuestionDelete
) 
from validator.views.causes import (
    CausesGet, CausesPost, CausesPut, ValidateView
)


app_name = 'validator'

urlpatterns = [
    # questions
    path('', QuestionGet.as_view({ "get": "get_all"}), name="get_question_list"),
    path('<uuid:pk>/', QuestionGet.as_view({ 'get': 'get' }), name="get_question"),
    path('search/', QuestionGet.as_view({ 'get': 'get_matched' }), name="get_matched"),
    path('pengawasan/', QuestionGet.as_view({ 'get': 'get_privileged' }), name="get_question_list_pengawasan"),
    path('baru/', QuestionPost.as_view(), name="create_question"),
    path('ubah/<uuid:pk>/', QuestionPut.as_view(), name="put_question"),
    # causes
    path('hapus/<uuid:pk>/', QuestionDelete.as_view(), name="delete_question"),
    path('causes/', CausesPost.as_view(), name="create_causes"),
    path('causes/<uuid:question_id>/<uuid:pk>', CausesGet.as_view(), name="get_causes"),
    path('causes/update/<uuid:question_id>/<uuid:pk>/', CausesPut.as_view(), name="put_causes"),
    path('causes/validate/<uuid:question_id>/', ValidateView.as_view(), name="validate_causes"),
]
