
# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
import secrets
from .serializers import RegisterSerializer, VerifySerializer, LoginSerializer
from django.core.mail import send_mail
from django.conf import settings

 
User = get_user_model()
 
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            one_time_token = secrets.token_hex(16)
            user.one_time_token = one_time_token
            user.save()
            return Response({'one_time_token': one_time_token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class VerifyView(APIView):
    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            one_time_token = serializer.validated_data['one_time_token']
            try:
                user = User.objects.get(username=username)
                if user.one_time_token == one_time_token and check_password(password, user.password):
                    user.is_verified = True
                    user.one_time_token = None
                    user.save()
                    return Response({'message': 'User verified'}, status=status.HTTP_200_OK)
                return Response({'message': 'Invalid credentials or token'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
 
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = request.data.get('email')
            otp = request.data.get('otp')
        
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password) and user.is_verified:
                   
                     
                    
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        #'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                return Response({'message': 'Invalid credentials or user not verified'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py

class VerifyEmailAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        token = request.data.get('token')
        
        # Validate the token (assuming you have stored it somewhere)
        # Perform the verification process
        
        # Example: Dummy verification for demonstration
        if token == 'generated_token_from_email':
            # Mark the user as verified (you can implement this logic based on your requirements)
            return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)
