FROM node:10

ADD src/chat /app

WORKDIR /app

RUN yarn install

ADD ./docker_config/chat/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]