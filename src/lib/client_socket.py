import socket
import sys

from .constant import DIRECTION, ACTION

class ClientSocket:
    def __init__(self, ip, port, verbose=True):
        self.ip = ip
        self.port = port
        self.verbose = verbose

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        if self.verbose:
            print('connecting to {}, port {}'
                      .format(self.ip, self.port))
        self.sock.connect((self.ip, self.port))

    def send(self, message):
        if self.verbose:
            print('sending message: {}'.format(message))
        try:
            self.sock.sendall(bytes(message, 'utf-8'))
        finally:
            print('did not manage to send message')

    def sendCmd(self, direction, action):
        self.send('{}{}'.format(
            DIRECTION[direction],
            ACTION[action]))

    def close(self):
        if self.sock.fileno() != -1:
            if self.verbose:
                print("closing socket")
            self.sock.close()
        elif self.verbose:
            print("attempted close() on closed socket")

    def __del__(self):
        self.close()
