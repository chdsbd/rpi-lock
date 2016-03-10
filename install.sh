#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd rpi-lock && \
sudo pip install -r requirements.txt && \
python sql_setup.py && \
cp -n example-rpi-lock.cfg rpi-lock.cfg &&\
(sudo crontab -l ; echo "@reboot bash $DIR/start-lock.sh") | sudo crontab -
