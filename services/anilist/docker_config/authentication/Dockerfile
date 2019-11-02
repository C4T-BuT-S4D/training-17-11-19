FROM python:3.7-alpine

RUN apk add gcc make musl-dev postgresql-dev

ADD src/authentication/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD src/authentication /app

ADD docker_config/authentication/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
