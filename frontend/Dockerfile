FROM python:3.9-slim

RUN pip install --no-cache-dir --upgrade pip

ENV APP_HOME=/home

EXPOSE 8080

WORKDIR $APP_HOME

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