# Flower Monitoring Service

A monitoring dashboard for tracking Celery worker performance in the subtitle generation system.

>The application only works with dependent applications, for this, redis and the target application of the celery **worker** must be running
## Overview
This service provides real-time monitoring and management of Celery tasks performed by the Subtitle Worker. It allows administrators to track task progress, view task history, and manage the worker queue.
>**Important:** This service requires the [**Worker**](https://github.com/shc0der/subtitles/tree/main/worker) service to be running. The Worker handles the actual subtitle extraction processing.

## Configuration
All variables must be registered in the .env file

## Getting Started
#### 1. Start the Worker Service
The Worker service must be running before starting this service. See the [Worker README](https://github.com/shc0der/subtitles/blob/main/worker/README.md) for setup instructions.

#### 2. Build the Monitoring
```
docker build -t subtitle_monitoring .
```

#### 3. Run the Monitoring
```
docker run --rm -d \
  --name=subtitle_monitoring_service \
  -p 5555:5555 \
  subtitle_monitoring
```

## Access Points
- **Monitoring Dashboard:** http://localhost:5555/

## How to perform tasks manually

Starting Tasks Manually:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"video_path":"/home/data/uploads/example.mp4"}' \
  http://localhost:5555/api/task/async-apply/task_video_processing
```
Terminating Tasks:
```bash
curl -X POST \
  -d 'terminate=True' \
  http://localhost:5555/api/task/revoke/<task-id-123456>
```


