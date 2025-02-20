from pydantic import BaseModel


class VideoData(BaseModel):
    video_path: str