from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import (
   AuthenticationFailed, ParseError
)
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from .models import CustomUser
from .serializers import (
    CustomUserSerializer, LoginRequestSerializer, LoginResponseSerializer, RegisterSerializer, EditUserSerializer
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
    request=RegisterSerializer,
)
@api_view(['POST'])
def register(request):
    """
    Register a new user.
    """ 
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@extend_schema(
    request=EditUserSerializer,
)
@api_view(['PATCH'])
def edit_user(request):
    """
    Edit username, email, and password of the logged-in user.
    """
    user = request.user
    
    if not user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = EditUserSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        requested_username = serializer.validated_data.get('username')
        requested_email = serializer.validated_data.get('email')
        requested_password = serializer.validated_data.get('password')

        if requested_username == user.username:
            return Response({"case_error": "New username cannot be the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)
        
        if requested_email == user.email:
            return Response({"case_error": "New email cannot be the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)

        if requested_username and CustomUser.objects.exclude(pk=user.pk).filter(username=requested_username).exists():
            return Response({"case_error": "This username is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        if requested_email and CustomUser.objects.exclude(pk=user.pk).filter(email=requested_email).exists():
            return Response({"case_error": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
        
        if requested_password and user.check_password(requested_password):
            return Response({"case_error": "New password cannot be the same as the current one."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        updated_user = CustomUser.objects.get(pk=user.pk)
        return Response({
            "username": updated_user.username,
            "email": updated_user.email
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
