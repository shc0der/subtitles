import os
import shutil
import uuid
from typing import Optional

from app.data.subtitle_receiver_session import SubtitleReceiverSession
from app.models.result import Result


class UploadFileUseCase:
    def __init__(self, upload_folder: str, subtitle_receiver_session: SubtitleReceiverSession):
        self._upload_folder = upload_folder
        self._subtitle_session = subtitle_receiver_session

    def execute(self, uploaded_file:Optional[str]):
        try:
            if uploaded_file is None:
                return Result.failure("File not found.")

            os.makedirs(self._upload_folder, exist_ok=True)

            if not self._subtitle_session.has_uploaded_video(uploaded_file):
                file_id = str(uuid.uuid4())
                file_name = os.path.basename(uploaded_file)
                file_path = os.path.join(self._upload_folder, f"{file_id}_{file_name}")

                shutil.copy(uploaded_file, file_path)

                self._subtitle_session.set_video_path(file_path)
            else:
                file_path = self._subtitle_session.get_video_path()

            return Result.success(file_path)
        except Exception as err:
            return Result.failure(f"An error occurred when uploading the video. {err}")
