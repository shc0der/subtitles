import os
import sys

from celery import Celery

from app.core.settings import Settings
from app.use_cases.extract_subtitles_use_case import ExtractSubtitlesUseCase

sys.path.append(os.path.abspath(os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])))


from injector import Injector

from app.di.app_module import AppModule


injector = Injector([AppModule()])
celery = injector.get(Celery)
settings = injector.get(Settings)
extract_subtitles_use_case = injector.get(ExtractSubtitlesUseCase)


@celery.task(bind=True, name=settings.CELERY_TASK_VIDEO_PROCESSING)
def video_processing(self, **kwargs):
    try:
        for part in extract_subtitles_use_case.execute(**kwargs):
            state = part.get("state", "")
            if state != "SUCCESS":
                self.update_state(state=state, meta=part)
            else:
                return part
    except Exception as e:
        self.update_state(state='ERROR', meta={"state":"ERROR", "message":str(e)})
        raise e
