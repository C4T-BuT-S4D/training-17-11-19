#!/bin/sh

set -e

#php artisan migrate && cd public && php-fpm

touch /db/database.sqlite || echo "DB already exists"

php artisan migrate && php -S 0.0.0.0:8000 -t public