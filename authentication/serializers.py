from rest_framework import serializers

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