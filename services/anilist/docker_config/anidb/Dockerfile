FROM phppm/nginx

RUN apk --no-cache add php7-sqlite3 php7-pdo_sqlite

ADD src/anidb /var/www/

ADD ./docker_config/anidb/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


CMD ["/entrypoint.sh"]
