from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from .models import User, UserSession
from .serializers import *
from .utils import generate_session_token

# Create your views here.

#Signup View
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status = status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email or password"},
                status = status.HTTP_401_UNAUTHORIZED
            )

        if user.auth_provider != "email":
            return Response(
                {"detail": f"This account uses {user.auth_provider} login. Please login using that method."},
                status = status.HTTP_400_BAD_REQUEST,
            )

        elif not user.check_password(password):
            return Response(
                {"detail": "Invalid email or password"},
                status = status.HTTP_401_UNAUTHORIZED,
            )

        raw_token, token_hash = generate_session_token()

        expires_at = timezone.now() + timedelta(hours = 24)

        UserSession.objects.create(
            user=user,
            token_hash = token_hash,
            expires_at=expires_at,
        )

        return Response(
            {
                "access_token": raw_token,
                "token_type": "Bearer",
                "expires_in": expires_at,
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "auth_provider": user.auth_provider,
                },
            },
            status = status.HTTP_200_OK,
        )