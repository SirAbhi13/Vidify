from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Video
from .serializers import VideoUploadSerializer


class AudioExtractionView(APIView):
    def post(self, request):
        serializer = VideoUploadSerializer(data=request.data)

        if serializer.is_valid():
            video_file = serializer.validated_data["file"]

            # Implement FFmpeg logic for audio extraction here
            # Extract audio from video_file and save it to an audio file

            # Assuming you've extracted audio and saved it as audio_file, you can then create a record in the database
            audio_file = "path/to/extracted/audio.wav"
            video = Video.objects.create(
                username=request.user.username,  # Assuming user is authenticated
                name=video_file.name,
                hash="unique_hash",  # You need to calculate a unique hash for this video
                size=video_file.size,
                uploaded_at=datetime.now(),
                file=audio_file,
            )

            return Response(
                {"audio_url": audio_file.url}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
