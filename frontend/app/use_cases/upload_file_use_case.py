import os
import uuid

from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.data.subtitle_receiver_session import SubtitleReceiverSession
from app.models.result import Result


class UploadFileUseCase:
    def __init__(self, upload_folder: str, subtitle_receiver_session: SubtitleReceiverSession):
        self._upload_folder = upload_folder
        self._subtitle_session = subtitle_receiver_session

    def execute(self, uploaded_file: UploadedFile):
        try:
            if not os.path.exists(self._upload_folder):
                os.makedirs(self._upload_folder)
            if not self._subtitle_session.has_uploaded_video(uploaded_file.name):
                file_id = str(uuid.uuid4())
                file_path = os.path.join(self._upload_folder, f"{file_id}_{uploaded_file.name}")
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                self._subtitle_session.set_uploaded_video(file_path)
            else:
                file_path = self._subtitle_session.get_video_path()

            return Result.success(file_path)
        except Exception as err:
            return Result.failure(f"An error occurred when uploading the video. {err}")
