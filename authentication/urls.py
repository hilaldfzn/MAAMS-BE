from django.urls import path

from .views import (
    login
)

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login')    
]