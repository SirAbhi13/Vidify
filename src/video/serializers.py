from django.core.validators import FileExtensionValidator
from rest_framework import serializers


class VideoSerializer(serializers.Serializer):
    video_file = serializers.FileField(
        # validators=[
        #     FileExtensionValidator(
        #         allowed_extensions=["mp4", "avi", "mkv", "mov", "wmv"]
        #     ),
        # ]
    )
