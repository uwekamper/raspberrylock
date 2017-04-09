#!/usr/bin/env python3

import time
from RPi import GPIO

OPEN_PIN = 15

def main():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(OPEN_PIN, GPIO.OUT)
	GPIO.output(OPEN_PIN, 0)
	GPIO.output(OPEN_PIN, 1)
	time.sleep(1.0)
	GPIO.output(OPEN_PIN, 0)

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
