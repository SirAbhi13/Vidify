from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Video(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    video_file = models.FileField(
        upload_to="src/video/videos",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "avi", "mkv", "mov", "wmv"]
            ),
        ],
    )
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.video_file.name}"


class ProcessedVideo(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    audio_file = models.CharField(max_length=255)
    extraction_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.video.video_file.name} - {self.audio_file.name}"
