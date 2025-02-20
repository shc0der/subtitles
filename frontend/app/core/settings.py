from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    UPLOAD_DIRECTORY:str = './data/uploads'

    CELERY_WORKER: str
    CELERY_BROKER_SERVER: str
    CELERY_BACKEND_SERVER: str
    CELERY_TASK_VIDEO_PROCESSING: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
