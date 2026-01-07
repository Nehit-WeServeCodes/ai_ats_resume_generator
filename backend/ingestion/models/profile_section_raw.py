import uuid
from django.db import models
from accounts.models import User

class ProfileSectionRaw(models.Model):
    SOURCE_CHOICES = (
        ("github", "GitHub"),
        ("resume", "Resume"),
        ("linkedin", "LinkedIn"),
        ("manual", "Manual"),
    )

    SECTION_CHOICES = (
        ("summary", "Summary"),
        ("skills", "Skills"),
        ("projects", "Projects"),
        ("experience", "Experience"),
        ("education", "Education"),
        ("achievements", "Achievements"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_section_raw")

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    section_type = models.CharField(max_length=50, choices = SECTION_CHOICES)

    raw_content = models.JSONField()

    soruce_ref_id = models.UUIDField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["section_type", "created_at"]

    def __str__(self):
        return f"{self.section_type} ({self.source})"