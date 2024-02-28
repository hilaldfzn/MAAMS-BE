from django.contrib.auth.hashers import check_password, make_password
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import (
   AuthenticationFailed, ParseError
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from drf_spectacular.utils import extend_schema

from .models import CustomUser
from .serializers import (
    CustomUserSerializer, LoginRequestSerializer, LoginResponseSerializer, RegisterSerializer
)


@extend_schema(
    description='Fill with valid username and password for an existing user.',
    request=LoginRequestSerializer,
    responses=LoginResponseSerializer,
)
@api_view(['POST'])
def login(request):
    """
    Process login credential requests.
    """
    try:
        username = request.data['username']
        password = request.data['password']

        user = get_object_or_404(
            CustomUser,
            username=username
        )
        # Check if password does not match
        if not check_password(password, user.password):
            raise AuthenticationFailed()
        
    # If request parameters are missing
    except KeyError:
        raise ParseError
    # If credentials are invalid
    except Http404:
        raise AuthenticationFailed()
    
    serializer = CustomUserSerializer(user)
    
    # If credentials are valid, then generate access and refresh tokens
    tokens = generate_tokens(user)
    # Return the tokens along with user details
    return Response(
        data={ 
            "access_token": tokens["access"],
            "refresh_token": tokens["refresh"],
            "data": serializer.data,
            "detail": "Successfully logged in."
        }, 
        status=status.HTTP_200_OK
    )
def generate_tokens(user: CustomUser) -> dict:
    """
    Generates access and refresh tokens for successful logins.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

@extend_schema(
    # description='Fill with valid username and password for an existing user.',
    request=RegisterSerializer,
)
@api_view(['POST'])
def register(request):
    """
    Register a new user.
    """
    if request.method == 'POST':  # Checking the request method
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Handling response when serializer is not valid
    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)  # Handling response when method is not allowed
