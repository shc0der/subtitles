FROM python:3.9-slim

EXPOSE 5555

ENV APP_HOME=/home

WORKDIR $APP_HOME

COPY ./app ${APP_HOME}/app
COPY ./.env ${APP_HOME}/
COPY ./requirements.txt ./
COPY ./docker-entrypoint.sh ./

RUN chmod +x ./docker-entrypoint.sh

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install -r requirements.txt &&\
    rm -rf /root/.cache/pip &&\
    rm requirements.txt


ENTRYPOINT ["./docker-entrypoint.sh"]