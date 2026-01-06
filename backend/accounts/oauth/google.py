import requests
from django.conf import settings

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def exchange_code_for_access_token(code: str) -> str:
    response = requests.post(
        GOOGLE_TOKEN_URL,
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        },
        timeout = 10,
    )
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_google_user(access_token: str) -> dict:
    response = requests.get(
        GOOGLE_USERINFO_URL,
        headers = {
            "Authorization": f"Bearer {access_token}"
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()