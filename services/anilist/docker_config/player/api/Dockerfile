FROM python:3.7-alpine

MAINTAINER @pomo_mondreganto

ENV PYTHONUNBUFFERED=1

RUN apk add gcc make musl-dev postgresql-dev

ADD src/player/api/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD src/player/api /app

ADD docker_config/player/api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
