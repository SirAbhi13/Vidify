from django.urls import path

from .views import AudioExtractionView, WatermarkVideoView

app_name = "video"

urlpatterns = [
    path("extract-audio/", AudioExtractionView.as_view(), name="audio-extract"),
    path("watermark-video/", WatermarkVideoView.as_view(), name="watermark-video"),
]
