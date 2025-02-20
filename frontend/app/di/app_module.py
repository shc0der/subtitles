from celery import Celery
from injector import Module, singleton, provider

from app.core.settings import Settings
from app.data.subtitle_receiver_session import SubtitleReceiverSession
from app.data.task_dispatcher import TaskDispatcher
from app.use_cases.upload_file_use_case import UploadFileUseCase


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
                    backend=settings.CELERY_BACKEND_SERVER)

    @singleton
    @provider
    def provide_task_dispatcher(self, celery: Celery, subtitle_session: SubtitleReceiverSession, settings: Settings) -> TaskDispatcher:
        return TaskDispatcher(celery, settings.CELERY_TASK_VIDEO_PROCESSING, subtitle_session)

    @singleton
    @provider
    def provide_upload_file_use_case(self, settings: Settings, subtitle_session: SubtitleReceiverSession) -> UploadFileUseCase:
        return UploadFileUseCase(settings.UPLOAD_DIRECTORY, subtitle_session)

    @singleton
    @provider
    def provide_subtitle_session_use_case(self) -> SubtitleReceiverSession:
        return SubtitleReceiverSession()
