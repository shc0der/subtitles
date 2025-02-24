import os
from typing import Optional

from injector import inject

import gradio as gr

from app.data.subtitle_receiver_session import SubtitleReceiverSession
from app.data.task_dispatcher import TaskDispatcher
from app.models.info_status import InfoStatus
from app.use_cases.upload_file_use_case import UploadFileUseCase
from app.utils.utils import parse_webvtt

css = """
#warning {background-color: #fcfae6; border-radius: 25px; padding: 10px;}
#success {background-color: #ebfaed; border-radius: 25px; padding: 10px; font-size: 4px !important}
#error {background-color: #fce9e6; border-radius: 25px; padding: 10px;}
"""

class Application:
    @inject
    def __init__(self, task_dispatcher: TaskDispatcher, upload_file_use_case: UploadFileUseCase, subtitle_receiver_session:SubtitleReceiverSession):
        self._task_dispatcher = task_dispatcher
        self._upload_file_use_case = upload_file_use_case
        self._subtitle_session = subtitle_receiver_session

    def _start_processing(self, video_file: Optional[str]):
        upload_result = self._upload_file_use_case.execute(video_file)
        if upload_result.is_successful():
            task_result = self._task_dispatcher.start_video_processing(upload_result.data)
            if task_result.is_successful():
                yield upload_result.data
            else:
               self._subtitle_session.set_message(task_result.message, InfoStatus.error)
        else:
            self._subtitle_session.set_message(upload_result.message, InfoStatus.error)

    def launch(self):
        with gr.Blocks(css=css) as demo:

            status_message = gr.Markdown(visible=False)
            with gr.Row():
                # Left column: upload and process control.
                with gr.Column(scale=1):
                    video_input = gr.File(label="Upload Video", file_types=[".mp4", ".mov", ".avi", ".mkv"])
                    process_button = gr.Button("Process Video")

                # Right column: display video and results.
                with gr.Column(scale=2):
                    video_player = gr.Video(label="Video Playback")
                    subtitles_table = gr.Dataframe(headers=["Start", "End", "Subtitle"], visible=True)

            process_button.click(
                self._start_processing,
                inputs=video_input,
                outputs=video_player
            )

            def poll_status():
                visible_message = False
                for status, message in self._subtitle_session.receive_messages():
                    visible_message = True
                    yield gr.update(value=message, elem_id=status.value, visible=visible_message), gr.update(visible=True)

                for state, payload in self._task_dispatcher.get_video_processing_state():
                    if state == "SUCCESS":
                        yield gr.update(visible=visible_message), gr.update(value=parse_webvtt(payload["subtitle_path"]))
                #yield gr.update(visible=visible_message), gr.update(visible=True)

            # The Interval component polls every 3 seconds (adjust as needed).
            timer =  gr.Timer(3)
            timer.tick(poll_status, outputs=[status_message, subtitles_table])


        demo.launch(server_name='0.0.0.0', server_port=8080, allowed_paths=[os.path.abspath("./../data/uploads")])
