import hashlib
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

from .models import UserSession

class SessionTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        raw_token = auth_header.split(" ")[1]
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        try:
            session = UserSession.objects.select_related("user").get(
                token_hash=token_hash,
                revoked=False,
                expires_at__gt=timezone.now(),
            )
        except UserSession.DoesNotExist:
            raise AuthenticationFailed("Invalid or expired token")

        return (session.user, session)