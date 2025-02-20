import os.path

from injector import inject

from app.data.audio_extractor import AudioExtractor
from app.data.subtitle_extractor import SubtitleExtractor


class ExtractSubtitlesUseCase:
    @inject
    def __init__(self, audio_extractor:AudioExtractor, subtitle_extractor: SubtitleExtractor):
        self._audio_extractor = audio_extractor
        self._subtitle_extractor = subtitle_extractor

    def execute(self, video_path: str, **kwargs):
        if os.path.exists(video_path):
            yield {"state": "PROGRESS", "message": "Start of audio track extraction."}
            audio_result = self._audio_extractor.extract(video_path)
            if audio_result.is_successful():
                yield {"state": "PROGRESS", "message": "Start of subtitle extraction."}
                subtitle_result = self._subtitle_extractor.extract(audio_result.data)
                if subtitle_result.is_successful():
                    data = {"video_path": video_path, "subtitle_path": subtitle_result.data}
                    yield {"state": "SUCCESS", "message": "Subtitles have been successfully extracted", "data":data}
            else:
                yield {"state": "ERROR", "message": "Couldn't extract audio track"}
        else:
            yield {"state": "ERROR", "message":"Video file not found"}