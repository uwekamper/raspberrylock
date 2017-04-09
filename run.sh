#!/bin/bash

aplay /opt/raspberrylock/bootup.wav

export PATH="/root/.local/bin:$PATH"
while true; do
    /usr/bin/python3 /opt/raspberrylock/schloss.py --theme default
    echo "Restarting raspberrylock.."
done
