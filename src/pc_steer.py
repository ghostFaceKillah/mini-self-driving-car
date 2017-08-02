import pygame
import sys
import threading

from lib.client_socket import ClientSocket
from lib.constant import *

def keydown(event):
    if event.key == pygame.K_UP:
        sock.sendCmd('up', 'start')
    if event.key == pygame.K_DOWN:
        sock.sendCmd('down', 'start')
    if event.key == pygame.K_RIGHT:
        sock.sendCmd('right', 'start')
    if event.key == pygame.K_LEFT:
        sock.sendCmd('left', 'start')

def keyup(event):
    if event.key == pygame.K_UP:
        sock.sendCmd('up', 'stop')
    if event.key == pygame.K_DOWN:
        sock.sendCmd('down', 'stop')
    if event.key == pygame.K_RIGHT:
        sock.sendCmd('right', 'stop')
    if event.key == pygame.K_LEFT:
        sock.sendCmd('left', 'stop')


class PygameDriver(threading.Thread):
    def __init__(self, ip, port, window_size):
        print('Starting pygame window, size: {}'.format(window_size),
              file=sys.stderr)
        pygame.init()
        pygame.display.set_mode(window_size)

        self.sock = ClientSocket(ip, port, True)

    def connect(self):
        print('Connecting to steering server',
              file=sys.stderr)
        self.sock.connect()

    def run(self):
        self.connect()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    keydown(event)
                if event.type == pygame.KEYUP:
                    keyup(event)
