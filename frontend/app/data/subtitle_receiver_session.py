from typing import Optional

import streamlit as st
from injector import inject
from streamlit.runtime.state import SessionStateProxy

from app.models.info_status import InfoStatus


class SubtitleReceiverSession:
    def __init__(self):
        self._session = self._setup_session(st.session_state)

    def should_load_video(self) -> bool:
        return self._session.should_load_video

    def set_video_loaded_state(self, state:bool):
        self._session.should_load_video = state

    def has_active_task(self) -> bool:
        return self._session.task_id is not None

    def has_uploaded_video(self, video_name: str) -> bool:
        if self._session.video_path is not None:
            return self._session.video_path.endswith(video_name)
        return False

    def set_uploaded_video(self, video_path: str):
        self._session.video_path = video_path

    def get_video_path(self) -> str:
        return self._session.video_path

    @staticmethod
    def _setup_session(session: SessionStateProxy):
        properties = ["task_id", "video_path", "processing_state", "info_message", "should_load_video"]
        for prop in properties:
            if prop not in session:
                session[prop] = None
        return session

    def set_task_id(self, task_id:Optional[str]):
        self._session.task_id = task_id

    def get_task_id(self):
        return self._session.task_id


    def set_info_message(self, message: str, status: InfoStatus = InfoStatus.info):
        self._session.info_message = {"status": status, "message": message}

    def get_info_message(self):
        return self._session.info_message or {}

    def set_processing_state(self, data):
        self._session.processing_state = data
