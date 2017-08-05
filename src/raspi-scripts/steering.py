import socket
import sys
import RPi.GPIO as GPIO
from time import sleep

import lib.constant as cnst

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('0.0.0.0', cnst.STEERING_PORT)
sock.bind(server_address)

GPIO.setmode(GPIO.BOARD)

Motor1A = 33
Motor1B = 35
Motor1E = 37

Motor2A = 38
Motor2B = 40
Motor2E = 36

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

def turn_right():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)

def stop_turning():
    GPIO.output(Motor1E, GPIO.LOW)


def turn_left():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)


def go_forward():
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)


def go_back():
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    GPIO.output(Motor2E, GPIO.HIGH)


def stop():
    GPIO.output(Motor2E, GPIO.LOW)


def interpret(msg):
    direction = cnst.REV_DIRECTION[msg[0]]
    action = cnst.REV_ACTION[msg[1]]

    if direction == 'up':
        if action == 'start':
            go_forward()
        elif action == 'stop':
            stop()

    elif direction == 'down':
        if action == 'start':
            go_back()
        elif action == 'stop':
            stop()

    elif direction == 'right':
        if action == 'start':
            turn_right()
        elif action == 'stop':
            stop_turning()

    elif direction == 'left':
        if action == 'start':
            turn_left()
        elif action == 'stop':
            stop_turning()

try:
    stop()
    stop_turning()
    while True:
        data, client_address = sock.recvfrom(16)

        interpret(data.decode(cnst.ENCODING))

finally:
    GPIO.cleanup()



