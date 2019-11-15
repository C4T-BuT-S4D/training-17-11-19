#!/bin/sh

set -e
cd /app
yarn install
yarn serve --port 3000
