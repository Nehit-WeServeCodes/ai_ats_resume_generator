import secrets
import hashlib
from rest_framework_simplejwt.tokens import AccessToken

def generate_session_token():
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    return raw_token, token_hash

def generate_jwt_for_user(user):
    token = AccessToken.for_user(user)

    jti = token["jti"]

    jti_hash = hashlib.sha256(jti.encode()).hexdigest()

    return {
        "jwt": str(token),
        "jti": jti,
        "jti_hash": jti_hash,
        "expires_at": token["exp"],
    }