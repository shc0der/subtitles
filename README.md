# Subtitles

An AI-powered application for generating subtitles from video content.


## Project Overview
This project consists of multiple components working together to create automated subtitles:
- **frontend**: Main web application interface
- **worker**: Background service that handles subtitle extraction
- **monitor** _(optional)_: Task monitoring dashboard
- **data**: Shared storage directory for file management

## Getting Started
#### 1. Clone the repository:
```
git clone https://github.com/shc0der/subtitles.git
cd subtitles
```
#### 2. Configure environment variables:
- Each component has its own **.env** file with required configuration
- Review and modify environment variables as needed for your environment
>**Important:** The **/data/uploads** directory must be mounted as a volume for both the application and worker services.
#### 3. Build & Run:
Start all services using Docker Compose:
```
docker-compose up --build
```
## Access Points
- **Web Application**: http://localhost:8080/
- **Monitoring Dashboard** _(optional)_: http://localhost:5555/
## Development Notes
- For standalone component execution, ensure all environment variables are properly configured
- The application and worker must share access to the same **/data/uploads** directory
