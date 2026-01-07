import uuid
from django.db import models
from accounts.models import User

class RawManualData(models.Model):
    SECTION_CHOICES = (
        ("summary", "Summary"),
        ("skills", "Skills"),
        ("projects", "Projects"),
        ("experience", "Experience"),
        ("education", "Education"),
        ("achievements", "Achievements"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manual_raw")

    section_type = models.CharField(max_length=20, choices=SECTION_CHOICES)
    content = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manual({self.section_type})"