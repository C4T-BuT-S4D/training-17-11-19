FROM pomomondreganto/aniparser:latest

MAINTAINER @pomo_mondreganto

ENV PYTHONUNBUFFERED=1

ADD src/player/internal/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD src/player/internal /app

ADD docker_config/player/internal/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
