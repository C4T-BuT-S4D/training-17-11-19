FROM webdevops/php-apache:alpine

ADD docker_config/anidb/vhost.conf /opt/docker/etc/httpd/vhost.conf
ADD src/anidb /app

RUN chmod -R o+rw /app
