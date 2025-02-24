from typing import Optional, Dict, Any

import gradio as gr

from app.models.info_status import InfoStatus


class SubtitleReceiverSession:
    def __init__(self):
        self._storage = gr.BrowserState({}, "video_cache")
        self._session = self._setup_session(self._storage.value or {})
        self._storage.value = self._session

    def has_active_task(self) -> bool:
        return self._session.get("task_id") is not None

    def has_uploaded_video(self, video_name: str) -> bool:
        if self._session.get("video_path") is not None:
            return self._session["video_path"].endswith(video_name)
        return False

    def set_video_path(self, video_path: str):
        self._session["video_path"] = video_path

    def get_video_path(self) -> str:
        return self._session.get("video_path")

    def set_subtitle_path(self, subtitle_path: str):
        self._session["subtitle_path"] = subtitle_path

    def get_subtitle_path(self) -> str:
        return self._session.get("subtitle_path")

    @staticmethod
    def _setup_session(session: Dict[str, Any]):
        properties = ["task_id", "video_path", "subtitle_path", "processing_state", "messages"]
        for prop in properties:
            if prop not in session:
                session[prop] = None
        return session

    def set_task_id(self, task_id:Optional[str]):
        self._session["task_id"] = task_id

    def get_task_id(self):
        return self._session.get("task_id")


    def set_message(self, message: str, status: InfoStatus = InfoStatus.success):
        self._session["messages"] = {"status": status, "message": message}

    def receive_messages(self):
        data = self._session.get("messages")
        if data:
            yield data.get("status"), data.get("message")

    def set_processing_state(self, data):
        self._session["processing_state"] = data

    def sync(self):
        pass
