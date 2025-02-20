# Subtitle Web Application

A web interface for generating AI-powered subtitles from video content.

## Overview
This application is part of a larger subtitles generation system. It provides the frontend interface for uploading videos and managing the subtitle creation process.
>**Important:** This application requires the [**Worker**](https://github.com/shc0der/subtitles/tree/main/worker) service to be running. The Worker handles the actual subtitle extraction processing.

## Configuration
All variables must be registered in the .env file

## Getting Started
#### 1. Start the Worker Service
The Worker service must be running before starting this application. See the [Worker README](https://github.com/shc0der/subtitles/blob/main/worker/README.md) for setup instructions.

#### 2. Build the Web Application
```
docker build -t subtitle_app .
```

#### 3. Run the Web Application
```
docker run --rm -d \
  --name=subtitle_app_service \
  -v $(pwd)/../data/uploads:/home/data/uploads \
  -p 8080:8080 \
  subtitle_app
```
The application requires a shared volume for handling uploaded files:
- **Host path:** ./../data/uploads
- **Container path:** /home/data/uploads

## Access Points
- **Web Application**: http://localhost:8080/

## Development Notes
- Ensure the Worker service is properly configured and accessible
- The shared data volume must be accessible by both this application and the Worker service



