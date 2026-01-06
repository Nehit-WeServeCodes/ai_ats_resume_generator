import requests
from django.conf import settings

GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"

def github_exchange_code_for_token(code: str) -> str:
    response = requests.post(
        GITHUB_TOKEN_URL,
        headers = {"Accept": "application/json"},
        data = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("access_token")

def fetch_github_user(access_token: str) -> dict:
    response = requests.get(
        GITHUB_USER_URL,
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        timeout = 10,
    )

    response.raise_for_status()
    return response.json()

def fetch_github_user_emails(access_token: str) -> list:
    response = requests.get(
        GITHUB_EMAILS_URL,
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        },
        timeout= 10,
    )
    response.raise_for_status()
    return response.json()