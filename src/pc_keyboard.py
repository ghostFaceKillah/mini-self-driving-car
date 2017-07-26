import socket
import sys
import time
import keyboard

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.192.51', 4567)             # RPI, port 100
print >>sys.stderr, 'connecting to %s port %s' % server_address


def send(msg):
    print 'sending "{}"'.format(msg)
    sock.sendto(msg, server_address)


def turn_right():
    send('rx')

def stop_turning():
    send('ro')


def turn_left():
    send('lx')


def go_forward():
    send('ux')


def stop():
    send('uo')
    print "Stopping the car"


def register_hooks():
    print "Registering hooks"
    keyboard.hook_key('up', keydown_callback=go_forward, keyup_callback=stop)
    keyboard.hook_key('left', keydown_callback=turn_left, keyup_callback=stop_turning)
    keyboard.hook_key('right', keydown_callback=turn_right, keyup_callback=stop_turning)
    print "Hooks registered"


try:
    register_hooks()
    while True:
        time.sleep(0.1)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

