#!/bin/sh

set -e
cd /app
yarn install
yarn build
rm -rf /front_build/*
cp -r dist/* /front_build
