import uuid
from django.db import models
from accounts.models import User

class RawLinkedInData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="linkedin_raw")

    profile_url = models.TextField(null=True, blank = True)
    raw_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LinkedInData({self.user.email})"


