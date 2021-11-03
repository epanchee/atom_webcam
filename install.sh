#!/bin/bash

set -eu

if ! envsubst --version &> /dev/null; then
	echo "Нужно установить пакет 'gettext'"
	exit 1
fi

declare USER="${1:-$(whoami)}"
declare INTERVAL="${2:-600}"
declare DEBUG="${3:-}"
declare WORKDIR="${4:-$(pwd)}"
declare SAVE_PATH="${5:-$(pwd)/data}"

pipenv install

systemctl stop atom_webcam.service &>/dev/null || true
systemctl stop atom_web.service &>/dev/null || true

export USER WORKDIR INTERVAL SAVE_PATH DEBUG
envsubst '$USER,$WORKDIR,$DEBUG,$INTERVAL,$SAVE_PATH' <atom_webcam.service.tmplt > /etc/systemd/system/atom_webcam.service

touch /var/log/atom_webcam.log
chown "$USER:$USER" /var/log/atom_webcam.log

envsubst '$USER' <logrotate.tmplt > /etc/logrotate.d/atom_webcam
systemctl enable atom_webcam.service

cp -av web/nginx.conf /etc/nginx/sites-available/atom_web.conf
ln -s /etc/nginx/sites-available/atom_web.conf /etc/nginx/sites-enabled/ || true
systemctl enable atom_web.service

systemctl start atom_webcam.service
systemctl start atom_web.service

echo "Проверьте, что все хорошо запустилось:"
echo "sudo systemctl status atom_webcam.service"

