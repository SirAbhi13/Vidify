from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Video(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    video_file = models.FileField(
        upload_to="src/video/media/videos",
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

    def get_audio_file_object(self):
        with open(self.audio_file, "rb") as file:
            yield file

    def __str__(self):
        return f"{self.video.video_file.name} - {self.audio_file}"


class WatermarkedVideo(models.Model):
    user = models.CharField(max_length=100)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watermark_image = models.ImageField(
        upload_to="src/video/media/images",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png"]),
        ],
    )
    watermarked_video_path = models.CharField(max_length=255)
    overlay_timestamp = models.DateTimeField(auto_now_add=True)
    lazy_position = models.CharField(max_length=20, null=True)
    custom_coordinate_X = models.IntegerField(null=True)
    custom_coordinate_Y = models.IntegerField(null=True)
    scale = models.DecimalField(max_digits=3, decimal_places=2, default=0.2)

    def __str__(self):
        return f"{self.video.video_file.name} - {self.watermark_image.name}"
