from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignupView.as_view(), name = "signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name = "logout"),
    path("github/login/", GitHubLoginView.as_view(), name = "github-login"),
    path("github/callback/", GitHubCallbackView.as_view(), name = "github-callback"),
]