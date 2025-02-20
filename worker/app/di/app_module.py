from celery import Celery
from injector import Module, singleton, provider

from app.core.settings import Settings
from app.data.audio_extractor import AudioExtractor
from app.data.subtitle_extractor import SubtitleExtractor

class AppModule(Module):
    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()

    @singleton
    @provider
    def provide_celery(self, settings: Settings) -> Celery:
        return Celery(settings.CELERY_WORKER,
                    broker=settings.CELERY_BROKER_SERVER,
                    backend=settings.CELERY_BACKEND_SERVER,
                    broker_connection_retry_on_startup=True)

    @singleton
    @provider
    def provide_audio_extractor(self) -> AudioExtractor:
        return AudioExtractor()

    @singleton
    @provider
    def provide_subtitle_extractor(self, settings: Settings) -> SubtitleExtractor:
        return SubtitleExtractor(settings.WHISPER_MODEL, settings.MODEL_CACHE_DIR)
