import socket
import sys
import RPi.GPIO as GPIO
from time import sleep 
import lib.constant as cnst

import threading
    
Motor1A = 36  # 16
Motor1B = 38  # 18
Motor1E = 40  # 22

Motor2A = 37  # 23
Motor2B = 35  # 21
Motor2E = 33  # 19

def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(Motor1A, GPIO.OUT)
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)

    GPIO.setup(Motor2A, GPIO.OUT)
    GPIO.setup(Motor2B, GPIO.OUT)
    GPIO.setup(Motor2E, GPIO.OUT)

class RpiDriver(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        print('setting up GPIO')
        setupGPIO()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = ('0.0.0.0', port)
        self.sock.bind(self.server_address)
    
    def listen(self):
        print('starting up on {}'.format(self.server_address))
        self.sock.listen(1)

    def run(self):
        self.listen()
        try: 
            while True:
                print('waiting for connections...')
                connection, client_address = self.sock.accept()
                try:
                    print('connection from {}'.format(client_address))
        
                    while True:
                        data = connection.recv(16)
                        print('received {}'.format(data))
                        interpret(data.decode(cnst.ENCODING)
                        if not data:
                            print('no more data')
                            raise Exception('get caught')
                finally:
                    connection.close()
        
        finally:
            print("Cleaning up GPIO")
            GPIO.cleanup()

def turn_right():
    print("Turning the steering right")
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)

def stop_turning():
    print("Stopping motor")
    GPIO.output(Motor1E, GPIO.LOW)


def turn_left():
    print("Turning the steering left")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)


def go_forward():
    print("Going forward")
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)

def stop():
    print("Stopping the car")
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
        print("Cant go back for now, ignoring")

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
