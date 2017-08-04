import pygame
import sys
import threading

from lib.client_socket import ClientSocket
from lib.constant import *



class PygameDriver(threading.Thread):
    def __init__(self, ip, port, window_size):
        threading.Thread.__init__(self)
        print('Starting pygame window, size: {}'.format(window_size),
              file=sys.stderr)
        pygame.init()
        pygame.display.set_mode(window_size)

        self.sock = ClientSocket(ip, port, True)

    def connect(self):
        print('Connecting to steering server',
              file=sys.stderr)
        self.sock.connect()

    def keydown(self, event):
        if event.key == pygame.K_UP:
            self.sock.sendCmd('up', 'start')
        if event.key == pygame.K_DOWN:
            self.sock.sendCmd('down', 'start')
        if event.key == pygame.K_RIGHT:
            self.sock.sendCmd('right', 'start')
        if event.key == pygame.K_LEFT:
            self.sock.sendCmd('left', 'start')
    
    def keyup(self, event):
        if event.key == pygame.K_UP:
            self.sock.sendCmd('up', 'stop')
        if event.key == pygame.K_DOWN:
            self.sock.sendCmd('down', 'stop')
        if event.key == pygame.K_RIGHT:
            self.sock.sendCmd('right', 'stop')
        if event.key == pygame.K_LEFT:
            self.sock.sendCmd('left', 'stop')

    def run(self):
        self.connect()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    self.keydown(event)
                if event.type == pygame.KEYUP:
                    self.keyup(event)
