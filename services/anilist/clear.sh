#!/bin/bash

CWD="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

rm -rf "${CWD}/docker_volumes/postgres"
rm -rf "${CWD}/docker_volumes/anime"
rm -rf "${CWD}/docker_volumes/mongodb"

echo "[+] Done!"
