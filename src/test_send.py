import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.192.51', 4567)             # RPI, port 100
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


MESSAGES = [
    'ux',
    'uo',

    'lx',
    'lo',

    'rx',
    'ro',
]



try:
    print "will send test packages"

    # Send data
    for msg in MESSAGES:
        print 'sending "{}"'.format(msg)
        sock.sendall(msg)
        time.sleep(0.5)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
