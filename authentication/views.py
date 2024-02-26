from rest_framework import status
from rest_framework.response import Response

def login(request):
    """
    Process login credential requests.
    """
    if request.method == 'POST':
        
        return Response(
            data={ 
                "access_token": "<access_token>",
                "refresh_token": "<access_token>",
                "data": "<user_data>",
                "detail": "Successfully logged in."
            }, 
            status=status.HTTP_200_OK
        )