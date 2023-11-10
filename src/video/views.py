from datetime import datetime

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Video
from .serializers import VideoSerializer


class AudioExtractionView(APIView):
    # parser_classes = [FileUploadParser]
    def post(self, request):
        # serializer = VideoSerializer(data={"video_file": request.FILES['video_file']})
        serializer = VideoSerializer(data=request.data)

        if serializer.is_valid():
            # create a video object
            video = Video.objects.create(
                user="tester",  # Assuming user is authenticated
                video_file=serializer.validated_data["video_file"],
            )

            # Implement FFmpeg logic for audio extraction here
            # Extract audio from video_file and save it to an audio file

            # Assuming you've extracted audio and saved it as audio_file, you can then create a record in the database
            # audio_file = "path/to/extracted/audio.wav"

            return Response({"audio_url": "succes"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"detail": "succes"}, status=status.HTTP_200_OK)
