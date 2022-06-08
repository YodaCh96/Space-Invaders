#!/usr/bin/python

import RPi.GPIO as GPIO
import time

PIN_M = 17
PIN_T = 27

GPIO.setmode(GPIO.BCM)
capacity = 0.000001
adj = 2.130620985
i = 0
t = 0

while True:
    GPIO.setup(PIN_M, GPIO.OUT)
    GPIO.setup(PIN_T, GPIO.OUT)
    GPIO.output(PIN_M, False)
    GPIO.output(PIN_T, False)
    time.sleep(0.2)
    GPIO.setup(PIN_M, GPIO.IN)
    time.sleep(0.2)

    GPIO.output(PIN_T, True)
    starttime = time.time()
    endtime = time.time()
    while (GPIO.input(PIN_M) == GPIO.LOW):
        endtime = time.time()
    timeDiff = endtime-starttime

    res = (timeDiff/capacity)*adj
    i = i + 1
    t = t + res
    if i==10:
        t = t/i
        print(t)
        i = 0
        t = 0
