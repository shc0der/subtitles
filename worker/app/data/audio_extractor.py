import os.path

from moviepy import VideoFileClip

from app.models.result import Result
from app.utils.utils import separate_path_and_name


class AudioExtractor:

    def extract(self, video_path: str):
        path, name = separate_path_and_name(video_path)
        try:
            audio_path = f"{path}/{name}.wav"
            if not os.path.exists(audio_path):
                video = VideoFileClip(video_path)
                video.audio.write_audiofile(audio_path)
                video.close()
            return Result.success(audio_path)
        except Exception as err:
            return Result.failure(str(err))
