from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Video(models.Model):
    username = models.CharField(max_length=100, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=64, unique=True)
    size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to="/to_process/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "avi", "mkv", "mov", "wmv"]
            ),
        ],
    )

    def __str__(self):
        return self.name
