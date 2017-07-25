import socket
import sys
import RPi.GPIO as GPIO
from time import sleep 

import lib.constant as cnst

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname())
server_address = ('0.0.0.0', cnst.KEYBOARD_EVENTS_PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

GPIO.setmode(GPIO.BOARD)

Motor1A = 36  # 16
Motor1B = 38  # 18
Motor1E = 40  # 22

Motor2A = 37  # 23
Motor2B = 35  # 21
Motor2E = 33  # 19

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

def turn_right():
    print "Turning the steering right"
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)

def stop_turning():
    print "Stopping motor"
    GPIO.output(Motor1E, GPIO.LOW)


def turn_left():
    print "Turning the steering left"
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)


def go_forward():
    print "Going forward"
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)

def stop():
    print "Stopping the car"
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
        print "Cant go back for now, ignoring"

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
        print 'waiting for connections...'
        connection, client_address = sock.accept()
        try:
            print 'connection from {}'.format(client_address)

            while True:
                data = connection.recv(16)
                print 'received {}'.format(data)
                interpret(data)
                if not data:
                    print 'no more data'
                    break
        finally:
            connection.close()

finally:
    print "Cleaning up GPIO"
    GPIO.cleanup()

