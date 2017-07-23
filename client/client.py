import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.192.51', 100)             # RPI, port 100
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    message = 'Uszanowanko!!!'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

