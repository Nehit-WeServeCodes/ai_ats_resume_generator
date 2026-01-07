import uuid
from django.db import models
from accounts.models import User

class RawResumeData(models.Model):
    FILE_TYPES  = (
        ("pdf", "PDF"),
        ("docx", "DOCX"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume_raw")

    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file_url = models.TextField()
    
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume({self.file_name})"