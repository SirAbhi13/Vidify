import os
import subprocess

from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProcessedVideo, Video
from .serializers import AudioExtractionSerializer


class AudioExtractionView(APIView):
    # parser_classes = [FileUploadParser]
    def post(self, request):
        # serializer = AudioExtractionSerializer(data={"video_file": request.FILES['video_file']})
        serializer = AudioExtractionSerializer(data=request.data)

        if serializer.is_valid():
            video = Video.objects.create(
                user="tester",  # Assuming user is authenticated
                video_file=serializer.validated_data["video_file"],
            )
            audio_path = self.extract_audio(video.video_file.path)

            processed_video = ProcessedVideo.objects.create(
                video=video, audio_file=audio_path
            )
            try:
                audio_file = open(audio_path, "rb")
                response = FileResponse(audio_file)
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{os.path.basename(audio_path)}"'
                response["Content-Type"] = "audio/mp3"
                return response
            except Exception:
                return Response(
                    {"Error": "Error sending audio file"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"detail": "succes"}, status=status.HTTP_200_OK)

    def extract_audio(self, video_path):
        audio_path = f"src/video/media/audios/audio_{os.path.basename(video_path).split('.')[0]}.mp3"
        subprocess.run(
            ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path]
        )
        return audio_path


# class WatermarkVideoView(APIView):

#     def post (self,request)
