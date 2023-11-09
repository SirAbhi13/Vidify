from django.urls import path

from .views import AudioExtractionView

app_name = "video"

urlpatterns = [
    path("extract-audio/", AudioExtractionView.as_view(), name="audio-extract"),
]
