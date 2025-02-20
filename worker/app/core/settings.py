from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_HOST: str

    CELERY_WORKER: str
    CELERY_BROKER_SERVER: str
    CELERY_BACKEND_SERVER: str
    CELERY_TASK_VIDEO_PROCESSING: str

    WHISPER_MODEL: str = "small"
    MODEL_CACHE_DIR: str = "/home/data/models/whisper"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
