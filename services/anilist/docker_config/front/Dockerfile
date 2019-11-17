FROM node:10

ADD ./front /app

ADD ./docker_config/front/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
