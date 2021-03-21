#!/bin/bash

set -eu

envsubst --version &> /dev/null

declare USER="${1:-$(whoami)}"
declare INTERVAL="${2:-600}"
declare DEBUG="${3:-}"
declare WORKDIR="${4:-$(pwd)}"
declare SAVE_PATH="${5:-$(pwd)/data}"

systemctl stop atom_webcam.service

export USER WORKDIR INTERVAL SAVE_PATH DEBUG
envsubst '$USER,$WORKDIR,$DEBUG,$INTERVAL,$SAVE_PATH' <atom_webcam.service.tmplt > /etc/systemd/system/atom_webcam.service

touch /var/log/atom_webcam.log
chown "$USER:$USER" /var/log/atom_webcam.log

unlink /etc/logrotate.d/atom_webcam &>/dev/null || true
ln -s "$(pwd)/logrotate" /etc/logrotate.d/atom_webcam
systemctl enable atom_webcam.service
systemctl start atom_webcam.service

echo "Проверьте, что все хорошо запустилось:"
echo "sudo systemctl status atom_webcam.service"

