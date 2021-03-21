#!/bin/bash

set -eu

envsubst --version &> /dev/null

declare USER="${1:-$(whoami)}"
declare INTERVAL="${2:-600}"
declare WORKDIR="${3:-$(pwd)}"
declare SAVE_PATH="${4:-$(pwd)/data}"

export USER WORKDIR INTERVAL SAVE_PATH
envsubst '$USER,$WORKDIR,$INTERVAL,$SAVE_PATH' <atom_webcam.service.tmplt > /etc/systemd/system/atom_webcam.service

echo "Теперь нужно запустить:"

echo "sudo systemctl enable atom_webcam.service"
echo "sudo systemctl start atom_webcam.service"

echo "И проверить, что все хорошо:"
echo "sudo systemctl status atom_webcam.service"

