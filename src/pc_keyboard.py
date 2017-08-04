import socket
import sys
import time
import keyboard

import lib.constant as cnst

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect the socket to the port where the server is listening
server_address = cnst.RASPI_IP, cnst.KEYBOARD_EVENTS_PORT

status = {
  'up_down': None,
  'left_right': None
}


def send(msg):
    print 'sending "{}"'.format(msg)
    sock.sendto(msg, server_address)


def turn_right():
    status['left_right'] = 'right'


def stop_turning():
    status['left_right'] = None


def turn_left():
    status['left_right'] = 'left'


def go_forward():
    status['up_down'] = 'forward'


def go_back():
    status['up_down'] = 'back'


def stop():
    status['up_down'] = None


def register_hooks():
    print "Registering hooks"
    keyboard.hook_key('up', keydown_callback=go_forward, keyup_callback=stop)
    keyboard.hook_key('down', keydown_callback=go_back, keyup_callback=stop)
    keyboard.hook_key('left', keydown_callback=turn_left, keyup_callback=stop_turning)
    keyboard.hook_key('right', keydown_callback=turn_right, keyup_callback=stop_turning)
    print "Hooks registered"


try:
    register_hooks()
    while True:
        time.sleep(0.1)

        # Send direction state
        if status['left_right'] == 'left':
            msg = cnst.msg('left', 'start')
        elif status['left_right'] == 'right':
            msg = cnst.msg('right', 'start')
        else:
            msg = cnst.msg('right', 'stop')

        send(msg)

        # Send start stop msg
        if status['up_down'] == 'forward':
            msg = cnst.msg('up', 'start')
        elif status['up_down'] == 'back':
            msg = cnst.msg('down', 'start')
        else:
            msg = cnst.msg('up', 'stop')

        send(msg)


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()