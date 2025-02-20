FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg

RUN pip install --no-cache-dir --upgrade pip

ENV APP_HOME=/home

WORKDIR $APP_HOME

RUN mkdir -p ${APP_HOME}/data/models/whisper
RUN mkdir -p ${APP_HOME}/data/uploads

COPY ./app ${APP_HOME}/app
COPY ./.env ${APP_HOME}/
COPY ./requirements.txt ./
COPY ./docker-entrypoint.sh ./

RUN chmod +x ./docker-entrypoint.sh

RUN pip install -r requirements.txt &&\
    rm -rf /root/.cache/pip &&\
    rm requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]