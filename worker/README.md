# Subtitle Extraction Worker

A Celery-based worker service that processes videos and generates AI-powered subtitles.

## Overview
This worker handles the computational aspects of subtitle generation using AI models. It processes jobs from a queue and produces subtitle files.
>**Dependency:** This service requires **Redis** as a message broker and result backend.

## Configuration
All variables must be registered in the **.env** file

## Getting Started

#### 1. Run the Redis:
```
docker run --rm -d \
  --name=redis_service \
  -p 6379:6379 \
  redis:alpine
```
#### 2. Build the Worker:
```
docker build -t subtitle_worker .
```

#### 3. Run the Worker
```
docker run --rm -d \
  --name=subtitle_worker_service \
  -v $(pwd)/../data/uploads:/home/data/uploads \
  -v $(pwd)/../data/model/whisper:/home/data/model/whisper \
  subtitle_worker
```
The worker requires two mounted volumes:
- **/home/data/uploads:** For accessing uploaded video files and storing generated subtitles
- **/home/data/model/whisper:** For storing AI model files

## Development Notes

- Ensure Redis is properly configured and accessible
- The worker requires significant computational resources for AI-based subtitle extraction
- The same ./../data/uploads directory should be mounted on both this worker and the web application


