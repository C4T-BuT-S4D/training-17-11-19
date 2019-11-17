FROM php:7.2-fpm-alpine

ADD src/anidb /var/www/html

WORKDIR /var/www/html

ADD ./docker_config/anidb/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


CMD ["/entrypoint.sh"]
