#!/bin/sh

set -e
cd /app

gunicorn app:app --bind 0.0.0.0:5000 --worker-class sanic.worker.GunicornWorker
