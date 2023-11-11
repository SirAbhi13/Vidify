import os
import subprocess

from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response

from .models import ProcessedVideo, Video, WatermarkedVideo

base_path = "src/video/media"


def extract_audio(video_path):
    """method to extract audio from the video file provided"""

    audio_path = (
        f"{base_path}/audios/audio_{os.path.basename(video_path).split('.')[0]}.mp3"
    )
    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path])
    return audio_path


def overlay_watermark_with_coords(watermark_path, video_path, x_cord, y_cord, scale):
    """method to overlay watermark when coordinates are provided"""
    extension = os.path.basename(video_path).split(".")[1]
    final_vid_path = f"{base_path}/watermarked_videos/overlayed_{os.path.basename(video_path).split('.')[0]}.{extension}"
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


def overlay_watermark_with_pos(watermark_path, video_path, lazy_pos, scale):
    """method to overlay watermark when position is provided"""
    pos = {
        "top-left": "overlay",
        "top-right": "overlay=(main_w-overlay_w):0",
        "bottom-left": "overlay=0:(main_h-overlay_h)",
        "bottom-right": "overlay=(main_w-overlay_w):(main_h-overlay_h)",
        "center": "overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2",
    }
    extension = os.path.basename(video_path).split(".")[1]
    final_vid_path = f"{base_path}/watermarked_videos/overlayed_{os.path.basename(video_path).split('.')[0]}.{extension}"
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
        ]
    )
    return final_vid_path


def save_data_watermarked_video(data, video, scale):
    """Create the WatermarkedVideo instance in db"""
    watermarked_video = WatermarkedVideo.objects.create(
        video=video, watermark_image=data["image_file"], scale=scale
    )

    return watermarked_video


def save_extra_data(
    watermarked_video_obj, watermarked_video_path, x_cord, y_cord, lazy_pos
):
    "Update the WatermarkedVideo instance in db with remaining fields."
    watermarked_video_obj.watermarked_video_path = watermarked_video_path
    watermarked_video_obj.custom_coordinate_X = x_cord
    watermarked_video_obj.custom_coordinate_Y = y_cord
    watermarked_video_obj.lazy_position = lazy_pos

    watermarked_video_obj.save()
    return


def generate_response(watermarked_video_path):
    """generate response for with watermarked video"""
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
