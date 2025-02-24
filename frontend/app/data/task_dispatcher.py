from typing import Any

from celery import Celery
from celery.result import AsyncResult

from app.data.subtitle_receiver_session import SubtitleReceiverSession
from app.models.info_status import InfoStatus
from app.models.result import Result
from app.models.video_data import VideoData


class TaskDispatcher:
    def __init__(self, celery: Celery, task_video_processing: str, subtitle_receiver_session:SubtitleReceiverSession) -> None:
        self._celery = celery
        self._task_video_processing = task_video_processing
        self._subtitle_session = subtitle_receiver_session

    def start_video_processing(self, video_path: str) -> Any:
        try:
            payload = VideoData(video_path=video_path)
            result = self._celery.send_task(self._task_video_processing, kwargs=payload.model_dump())

            task_id = str(result.id)
            self._subtitle_session.set_task_id(task_id)

            return Result.success(task_id)
        except Exception as err:
            return Result.failure(f"Something went wrong with the task launch. {err}")

    def get_video_processing_state(self):
        task_id = self._subtitle_session.get_task_id()
        if task_id is not None:
            result = AsyncResult(task_id, app=self._celery)
            state = result.state
            if state == "PENDING":
                self._subtitle_session.set_message("The task has been queued, and the launch is expected...")
            elif state == "PROGRESS":
                meta = result.info or {}
                self._subtitle_session.set_message(meta.get("message") or "")
            elif state == "SUCCESS":
                payload, data = result.result, result.result["data"]
                self._subtitle_session.set_task_id(None)
                self._subtitle_session.set_message(payload.get("message") or "")
                self._subtitle_session.set_subtitle_path(data["subtitle_path"])
                yield state, data
            elif state == "ERROR":
                meta = result.info or {}
                self._subtitle_session.set_task_id(None)
                self._subtitle_session.set_message(meta.get("message") or "", InfoStatus.error)
            elif state == "FAILURE":
                self._subtitle_session.set_task_id(None)
                self._subtitle_session.set_message("An error occurred while processing the video!", InfoStatus.error)
