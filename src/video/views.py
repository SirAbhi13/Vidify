import os
import subprocess

from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProcessedVideo, Video, WatermarkedVideo
from .serializers import AudioExtractionSerializer, WatermarkSerializer


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

    def extract_audio(self, video_path):
        audio_path = f"src/video/media/audios/audio_{os.path.basename(video_path).split('.')[0]}.mp3"
        subprocess.run(
            ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path]
        )
        return audio_path


class WatermarkVideoView(APIView):
    def post(self, request):
        serializer = WatermarkSerializer(data=request.data)

        if serializer.is_valid():
            video = Video.objects.create(
                user="tester",
                video_file=serializer.validated_data["video_file"],
            )
            x_cord = serializer.validated_data.get("custom_coordinate_X")
            y_cord = serializer.validated_data.get("custom_coordinate_Y")
            lazy_pos = serializer.validated_data.get("lazy_position")
            scale = serializer.validated_data.get("scale", 0.2)

            if x_cord is not None and y_cord is not None:
                watermarked_video = self.save_data_watermarked_video(
                    serializer.validated_data, video, scale
                )

                watermarked_video_path = self.overlay_watermark_with_coords(
                    watermarked_video.watermark_image.path,
                    video.video_file.path,
                    x_cord,
                    y_cord,
                    scale,
                )

                self.save_extra_data(
                    watermarked_video, watermarked_video_path, x_cord, y_cord, lazy_pos
                )

                return self.generate_response(watermarked_video_path)
            elif lazy_pos is not None:
                watermarked_video = self.save_data_watermarked_video(
                    serializer.validated_data, video, scale
                )
                watermarked_video_path = self.overlay_watermark_with_pos(
                    watermarked_video.watermark_image.path,
                    video.video_file.path,
                    lazy_pos,
                    scale,
                )

                self.save_extra_data(
                    watermarked_video, watermarked_video_path, x_cord, y_cord, lazy_pos
                )

                return self.generate_response(watermarked_video_path)

            else:
                return Response(
                    {
                        "Error": "Need to provide either 'custom_coordinate_X and 'custom_coordinate_Y or 'lazy_position'"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def overlay_watermark_with_coords(
        self, watermark_path, video_path, x_cord, y_cord, scale
    ):
        extension = os.path.basename(video_path).split(".")[1]
        final_vid_path = f"src/video/media/watermarked_videos/overlayed_{os.path.basename(video_path).split('.')[0]}.{extension}"
        # ffmpeg -i test_file.mp4 -i GitHub-logo.png -filter_complex "[1][0]scale2ref=oh*mdar:ih*0.1[logo][video];[video][logo]overlay=10:20" output_scaled1-0topleft1.mp4

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-i",
                watermark_path,
                "-filter_complex",
                f"[1][0]scale2ref=oh*mdar:ih*{scale}[logo][video];[video][logo]overlay={x_cord}:{y_cord}",  # noqa: E231
                final_vid_path,
            ]
        )
        return final_vid_path

    def overlay_watermark_with_pos(self, watermark_path, video_path, lazy_pos, scale):
        pos = {
            "top-left": "overlay",
            "top-right": "overlay=(main_w-overlay_w):0",
            "bottom-left": "overlay=0:(main_h-overlay_h)",
            "bottom-right": "overlay=(main_w-overlay_w):(main_h-overlay_h)",
            "center": "overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2",
        }
        extension = os.path.basename(video_path).split(".")[1]
        final_vid_path = f"src/video/media/watermarked_videos/overlayed_{os.path.basename(video_path).split('.')[0]}.{extension}"

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-i",
                watermark_path,
                "-filter_complex",
                f"[1][0]scale2ref=oh*mdar:ih*{scale}[logo][video];[video][logo]{pos[lazy_pos]}",  # noqa: E231
                final_vid_path,
                final_vid_path,
            ]
        )
        return final_vid_path

    def save_data_watermarked_video(self, data, video, scale):
        watermarked_video = WatermarkedVideo.objects.create(
            user="tester", video=video, watermark_image=data["image_file"], scale=scale
        )

        return watermarked_video

    def save_extra_data(
        self, watermarked_video_obj, watermarked_video_path, x_cord, y_cord, lazy_pos
    ):
        watermarked_video_obj.watermarked_video_path = watermarked_video_path
        watermarked_video_obj.custom_coordinate_X = x_cord
        watermarked_video_obj.custom_coordinate_Y = y_cord
        watermarked_video_obj.lazy_position = lazy_pos

        watermarked_video_obj.save()
        return

    def generate_response(self, watermarked_video_path):
        try:
            final_vid_file = open(watermarked_video_path, "rb")
            response = FileResponse(final_vid_file)
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{os.path.basename(watermarked_video_path)}"'
            response["Content-Type"] = "video/mp4"
            return response
        except Exception:
            return Response(
                {"Error": "Error sending video file"},
                status=status.HTTP_404_NOT_FOUND,
            )
