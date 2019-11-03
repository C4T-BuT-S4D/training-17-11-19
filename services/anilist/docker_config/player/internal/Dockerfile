FROM pomomondreganto/aniparser:latest

RUN apk add make

ADD src/player/internal/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD src/player/internal /app

ADD docker_config/player/api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
