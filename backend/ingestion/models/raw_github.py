import uuid
from django.db import models
from accounts.models import User

class RawGitHubData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="github_raw")

    github_username = models.CharField(max_length=255)
    profile_json = models.JSONField()
    repos_json = models.JSONField()
    languages_json = models.JSONField(null=True, blank=True)
    readems_json = models.JSONField(null=True, blank = True)

    fetched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"GitHubData({self.github_username})"