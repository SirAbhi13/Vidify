import os

from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from video.models import ProcessedVideo, Video, WatermarkedVideo
from video.processing_utils import (
    extract_audio,
    generate_response,
    overlay_watermark_with_coords,
    overlay_watermark_with_pos,
    save_data_watermarked_video,
    save_extra_data,
)
from video.serializers import AudioExtractionSerializer, WatermarkSerializer

authentication = getattr(settings, "AUTHENTICATION", True)


class AudioExtractionView(APIView):
    """Logic for audio extraction"""

    permission_classes = (IsAuthenticated if authentication else AllowAny,)

    def post(self, request):
        serializer = AudioExtractionSerializer(data=request.data)

        if serializer.is_valid():
            video = Video.objects.create(
                user=request.user,  # Assuming user is authenticated
                video_file=serializer.validated_data["video_file"],
            )
            audio_path = extract_audio(video.video_file.path)

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


class WatermarkVideoView(APIView):
    """Logic for watermarking Video"""

    permission_classes = (IsAuthenticated if authentication else AllowAny,)

    def post(self, request):
        serializer = WatermarkSerializer(data=request.data)

        if serializer.is_valid():
            video = Video.objects.create(
                user=request.user,
                video_file=serializer.validated_data["video_file"],
            )
            x_cord = serializer.validated_data.get("custom_coordinate_X", None)
            y_cord = serializer.validated_data.get("custom_coordinate_Y", None)
            lazy_pos = serializer.validated_data.get("lazy_position", None)
            scale = serializer.validated_data.get("scale", 0.2)

            if x_cord is not None and y_cord is not None:
                watermarked_video = save_data_watermarked_video(
                    serializer.validated_data, video, scale
                )

                watermarked_video_path = overlay_watermark_with_coords(
                    watermarked_video.watermark_image.path,
                    video.video_file.path,
                    x_cord,
                    y_cord,
                    scale,
                )

                save_extra_data(
                    watermarked_video, watermarked_video_path, x_cord, y_cord, lazy_pos
                )

                return generate_response(watermarked_video_path)
            elif lazy_pos is not None:
                watermarked_video = save_data_watermarked_video(
                    serializer.validated_data, video, scale
                )
                watermarked_video_path = overlay_watermark_with_pos(
                    watermarked_video.watermark_image.path,
                    video.video_file.path,
                    lazy_pos,
                    scale,
                )

                save_extra_data(
                    watermarked_video, watermarked_video_path, x_cord, y_cord, lazy_pos
                )

                return generate_response(watermarked_video_path)

            else:
                return Response(
                    {
                        "Error": "Need to provide either 'custom_coordinate_X and 'custom_coordinate_Y or 'lazy_position'"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
