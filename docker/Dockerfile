FROM python:3.12.3-alpine3.20


ENV INSTALL_PATH /src
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk add --update --no-cache libpq libjpeg-turbo curl
RUN python -m pip install --upgrade pip


COPY ../requirements.txt .

RUN pip install -r requirements.txt
RUN adduser -u 999 -S appuser -s /bin/sh

COPY .. .
