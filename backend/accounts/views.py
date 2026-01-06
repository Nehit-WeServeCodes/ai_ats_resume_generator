from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.utils import timezone
from django.shortcuts import redirect
from django.conf import settings
from datetime import timedelta

from .models import User, UserSession
from .serializers import *
from .utils import *
from .authentication import *
from .oauth.github import *
from .oauth.google import *

# Create your views here.

#Signup View
class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status = status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#Login View
class LoginView(APIView):
    permission_classes = [AllowAny]
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

        # raw_token, token_hash = generate_session_token()

        # expires_at = timezone.now() + timedelta(hours = 24)

        jwt_data = generate_jwt_for_user(user)

        UserSession.objects.create(
            user=user,
            token_hash = jwt_data["jti_hash"],
            expires_at=timezone.now() + timedelta(hours=24),
        )

        return Response(
            {
                "access_token": jwt_data["jwt"],
                "token_type": "Bearer",
                "expires_in": jwt_data["expires_at"],
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "auth_provider": user.auth_provider,
                },
            },
            status = status.HTTP_200_OK,
        )

#Logout View
class LogoutView(APIView):
    authentication_classes = [HybridJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session = request.auth
        session.revoked = True
        session.save(update_fields=["revoked"])

        return Response(
            {"message": "Logged out successfully"},
            status = status.HTTP_200_OK,
        )

# GitHub Login View
class GitHubLoginView(APIView):
    permission_classes = []

    def get(slef, request):
        github_auth_url = (
            "https://github.com/login/oauth/authorize"
            f"?client_id={settings.GITHUB_CLIENT_ID}"
            "&scope=read:user user:email"
        )
        return redirect(github_auth_url)

# GitHub Callback View
class GitHubCallbackView(APIView):
    permission_classes = []

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response(
                {
                    "detail": "Authorization code missing."
                },
                status = status.HTTP_400_BAD_REQUEST,
            )

        try:
            access_token = exchange_code_for_access_token(code)
            github_user = fetch_github_user(access_token)

        except Exception:
            return Response(
                {"detail": "GitHub authentication failed"},
                status = status.HTTP_400_BAD_REQUEST,
            )

        github_id = str(github_user.get("id"))
        email = github_user.get("email")

        if not email:
            emails = fetch_github_user_emails(access_token)
            primary_emails = [
                e["email"] for e in emails if e.get("primary") and e.get("verified")
            ]
            if primary_emails:
                email = primary_emails[0]

        if not email:
            return Response(
                {"detail": "No verified email found in GitHub account."},
                status = status.HTTP_400_BAD_REQUEST,
            )

        user = None
        if User.objects.filter(github_id = github_id).exists():
            user = User.objects.get(github_id = github_id)

        elif User.objects.filter(email = email).exists():
            user = User.objects.get(email=email)
            user.github_id = github_id
            user.auth_provider = "github"
            user.save(update_fields=["github_id", "auth_provider"])

        else:
            user = User.objects.create(
                email = email,
                github_id = github_id,
                auth_provider = "github",
            )

        # raw_token, token_hash = generate_session_token()
        # expires_at = timezone.now() + timedelta(hours = 24)

        jwt_data = generate_jwt_for_user(user)

        UserSession.objects.create(
            user = user, 
            token_hash = jwt_data["jti_hash"],
            expires_at = timezone.now() + timedelta(hours = 24),
        )

        return Response(
            {
                "access_token": jwt_data["jwt"],
                "token_type": "Bearer",
                "expires_at": jwt_data["expires_at"],
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "auth_provider": user.auth_provider,
                },
            },
            status = status.HTTP_200_OK,
        )

#Google Login View
class GoogleLoginView(APIView):
    permission_classes = []

    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={settings.GOOGLE_CLIENT_ID}"
            "&response_type=code"
            "&scope=openid email profile"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            "&prompt=select_account"
        )
        return redirect(google_auth_url)

#Google Callback View
class GoogleCallbackView(APIView):
    permission_classes = []

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response(
                {"detail":"Authorization code missing."},
                status = status.HTTP_400_BAD_REQUEST,
            )

        try:
            access_token = exchange_code_for_access_token(code)
            google_user = fetch_google_user(access_token)
        except Exception:
            return Response(
                {"detail": "Google authentication failed"},
                status = status.HTTP_400_BAD_REQUEST,
            )

        google_id = str(google_user.get("id"))
        email = google_user.get("email")

        if not email or not google_id:
            return Response(
                {"detail": "Invalid Google user data"},
                status = status.HTTP_400_BAD_REQUEST,
            )

        user = None
        if User.objects.filter(google_id = google_id).exists():
            user = User.objects.get(google_id = google_id)

        elif User.objects.filter(email = email).exists():
            user = User.objects.get(email=email)
            user.google_id = google_id
            user.auth_provider = "google"
            user.save(update_fields=["google_id", "auth_provider"])

        else:
            user = User.objects.create(
                email = email,
                google_id= google_id,
                auth_provider = "google",
            )

        # raw_token, token_hash = generate_session_token()
        # expires_at = timezone.now() + timedelta(hours = 24)

        jwt_data = generate_jwt_for_user(user)

        UserSession.objects.create(
            user = user, 
            token_hash = jwt_data["jti_hash"],
            expires_at = timezone.now() + timedelta(hours = 24),
        )

        return Response(
            {
                "access_token": jwt_data["jwt"],
                "token_type": "Bearer",
                "expires_at": jwt_data["expires_at"],
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "auth_provider": user.auth_provider,
                },
            },
            status = status.HTTP_200_OK,
        )