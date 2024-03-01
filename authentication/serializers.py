from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid', 'username', 'email', 
            'first_name', 'last_name', 'date_joined',
            'is_active'
        ]


class LoginRequestSerializer(serializers.Serializer):
    class Meta:
        ref_name = 'login_request'
        fields = ('username', 'password')
    
    username = serializers.CharField()
    password = serializers.CharField()
    

class LoginResponseSerializer(serializers.Serializer):
    class Meta:
        ref_name = 'login_response'
        fields = ('access_token', 'refresh_token', 'data', 'detail')
    
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    data = CustomUserSerializer()
    detail = ''

    
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]  # Menambahkan UniqueValidator untuk memastikan email adalah unik
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


