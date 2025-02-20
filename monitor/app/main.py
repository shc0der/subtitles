import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

CELERY_WORKER = os.getenv("CELERY_WORKER")
CELERY_BROKER_SERVER = os.getenv("CELERY_BROKER_SERVER")
CELERY_BACKEND_SERVER = os.getenv("CELERY_BACKEND_SERVER")

celery = Celery(CELERY_WORKER,
                broker=CELERY_BROKER_SERVER,
                backend=CELERY_BACKEND_SERVER,
                broker_connection_retry_on_startup=True)
