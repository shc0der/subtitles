import os.path

import whisper

from app.models.result import Result
from app.utils.utils import separate_path_and_name


class SubtitleExtractor:

    def __init__(self, whisper_model: str = "small", cache_dir: str = "/home/data/models/whisper"):
        self._model = whisper.load_model(whisper_model, download_root=os.path.abspath(cache_dir))

    def extract(self, audio_path: str):
        path, name = separate_path_and_name(audio_path)
        try:
            subtitle_path = f"{path}/{name}.vtt"
            if not os.path.exists(subtitle_path):
                subtitles = self._transcribe_audio(audio_path)
                self._save_subtitles(subtitles, subtitle_path)

            return Result.success(subtitle_path)
        except Exception as err:
            return Result.failure(str(err))

    def _transcribe_audio(self, audio_path: str):
        result = self._model.transcribe(audio=audio_path)
        return self._convert_to_vtt_subtitles(result)

    @staticmethod
    def _convert_to_vtt_subtitles(result: dict) -> str:
        def format_time(seconds):
            milliseconds = int(seconds * 1000)
            hours, remainder = divmod(milliseconds, 3600000)
            minutes, remainder = divmod(remainder, 60000)
            seconds, milliseconds = divmod(remainder, 1000)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

        subtitles = "WEBVTT\n\n"
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]

            # Format VTT subtitle line
            subtitle_line = f"{segment['id']}\n"
            subtitle_line += f"{format_time(start_time)} --> {format_time(end_time)}\n"
            subtitle_line += f"{text}\n\n"

            subtitles += subtitle_line
        return subtitles

    @staticmethod
    def _save_subtitles(subtitles:str, subtitle_file:str):
        with open(subtitle_file, "w") as out_file:
            out_file.write(subtitles)
