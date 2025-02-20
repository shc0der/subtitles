from typing import Optional

import streamlit as st

from injector import inject
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.data.subtitle_receiver_session import SubtitleReceiverSession
from app.data.task_dispatcher import TaskDispatcher
from app.models.info_status import InfoStatus
from app.use_cases.upload_file_use_case import UploadFileUseCase
from app.utils.utils import parse_webvtt


class Application:
    @inject
    def __init__(self, task_dispatcher: TaskDispatcher, upload_file_use_case: UploadFileUseCase, subtitle_receiver_session:SubtitleReceiverSession):
        self._task_dispatcher = task_dispatcher
        self._upload_file_use_case = upload_file_use_case
        self._subtitle_session = subtitle_receiver_session
        self._video_player = None
        self._subtitles_table = None

    def _info(self, message: str):
        self._subtitle_session.set_info_message(message)

    def _error(self, message: str):
        self._subtitle_session.set_info_message(message, InfoStatus.error)

    def _show_subtitles(self, subtitle_path:str):
        if self._subtitles_table:
            df = parse_webvtt(subtitle_path)
            self._subtitles_table.table(df)
        else:
            self._error("The subtitle table was not created.")

    def _play_video(self, video_path: str, subtitle_path: Optional[str] = None):
        if self._video_player:
            self._video_player.video(video_path, subtitles = subtitle_path)
        else:
            self._error("The video player was not created.")

    def _start_task_of_getting_subtitles(self, video_path: str):
        self._play_video(video_path)

        result = self._task_dispatcher.video_processing(video_path)
        if result.is_successful():
            self._info("Video processing is running. Wait for execution...")
        else:
            self._error(result.message)

    def _submit_video(self, uploaded_file: UploadedFile):
        if not self._subtitle_session.has_active_task():
            result = self._upload_file_use_case.execute(uploaded_file)
            if result.is_successful():
                self._start_task_of_getting_subtitles(result.data)
            else:
                self._error(result.messsage)

    def _on_start_upload_click(self):
        self._subtitle_session.set_video_loaded_state(True)

    @st.fragment(run_every=2)
    def _monitor_ui(self):
        info = self._subtitle_session.get_info_message()
        status, message = info.get("status", ""), info.get("message", "")

        if status == InfoStatus.info:
            st.info(message)
        elif status == InfoStatus.error:
            st.error(message)
        elif status:
            st.warning(message)

        for task_info in self._task_dispatcher.video_processing_info():
            result = task_info.get("result")
            if task_info.get("state", "") == "SUCCESS" and result:
                data = result["data"]
                self._play_video(data["video_path"], data["subtitle_path"])
                self._show_subtitles(data["subtitle_path"])

    @st.fragment()
    def _left_side_ui(self):
        st.markdown("**Upload a video**")
        with st.container(border=True, height=500):
            uploaded_file = st.file_uploader("Select a video file:", type=["mp4", "mov", "avi"])
            st.button("Recognize", on_click=self._on_start_upload_click, use_container_width=True)
            if self._subtitle_session.should_load_video():
                self._subtitle_session.set_video_loaded_state(False)
                if uploaded_file is not None:
                    self._submit_video(uploaded_file)
                else:
                    self._error("Please select the video file.")

    def _right_side_ui(self):
        st.markdown("**Video & Subtitles**")
        with st.container(border=True, height=500):
            self._video_player = st.empty()
            self._subtitles_table = st.empty()

    def launch(self):
        st.set_page_config(page_title="The creator of subtitles", layout="wide")

        self._monitor_ui()

        left_col, right_col = st.columns([1,3])
        with left_col:
            self._left_side_ui()
        with right_col:
            self._right_side_ui()
