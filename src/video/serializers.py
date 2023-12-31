from django.core.validators import FileExtensionValidator
from rest_framework import serializers


class AudioExtractionSerializer(serializers.Serializer):
    """Validates the request recieved for audio-extraction endpoint"""

    video_file = serializers.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "avi", "mkv", "mov", "wmv"]
            ),
        ]
    )


class WatermarkSerializer(serializers.Serializer):
    """Validates the request recieved for watermark-video endpoint"""

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

    lazy_position = serializers.CharField(max_length=20, required=False)
    custom_coordinate_X = serializers.IntegerField(required=False)
    custom_coordinate_Y = serializers.IntegerField(required=False)
    scale = serializers.DecimalField(max_digits=3, decimal_places=3, required=False)

    def validate_lazy_position(self, value):
        """Validates that lazy_position is from defines values only"""
        lp = ["top-right", "top-left", "bottom-right", "bottom-left", "center"]
        if value is not None and value not in lp:
            raise serializers.ValidationError(
                "Not a valid lazy position. Acceptable positions are top-left, top-right, bottom-left, bottom-right and center"
            )
        return value

    def validate_scale(self, value):
        """Validates the value of scale is less than 1"""
        if value > 1.0:
            raise serializers.ValidationError("Value of scale should be less than 1")
        return value
