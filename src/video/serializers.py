from django.core.validators import FileExtensionValidator
from rest_framework import serializers


class AudioExtractionSerializer(serializers.Serializer):
    user = serializers.CharField(required=True, max_length=50)
    video_file = serializers.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "avi", "mkv", "mov", "wmv"]
            ),
        ]
    )


class WatermarkSerializer(serializers.Serializer):
    user = serializers.CharField(required=True, max_length=50)
    video_file = serializers.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "avi", "mkv", "mov", "wmv"]
            ),
        ]
    )
    image_file = serializers.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpg"]),
        ]
    )

    lazy_position = serializers.CharField(max_length=20)
    custom_coordinate_X = serializers.IntegerField()
    custom_coordinate_Y = serializers.IntegerField()
    scale = serializers.DecimalField(max_digits=3, decimal_places=2)
