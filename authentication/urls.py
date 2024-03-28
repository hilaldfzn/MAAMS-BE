from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView
)

from .views import (
    login, 
    register,
    edit_user
)

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),    
    path('register/', register, name='register'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('update/', edit_user, name='update')
]
