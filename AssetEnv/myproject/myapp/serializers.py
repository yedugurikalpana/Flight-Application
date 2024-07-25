from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
 
User = get_user_model()
 
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}
 
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
 
class VerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    one_time_token = serializers.CharField()
 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()