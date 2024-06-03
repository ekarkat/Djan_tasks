FROM python:3.12.3-alpine3.20

RUN mkdir -p /home/app
WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache libpq libjpeg-turbo curl
RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

COPY docker/app_entrypoint.sh /home/app/app_entrypoint.sh
RUN chmod +x /home/app/app_entrypoint.sh

COPY docker/celery_enterypoint.sh /home/app/celery_enterypoint.sh
RUN chmod +x /home/app/celery_enterypoint.sh
