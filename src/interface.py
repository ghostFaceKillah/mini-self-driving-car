import pygame
import sys

from client import ClientSocket
from constant import *

pygame.init()
pygame.display.set_mode((100, 100))

rpi = "192.168.192.51"
port = 4567
sock = ClientSocket(rpi, port, True)
sock.connect()

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            keydown(event)
        if event.type == pygame.KEYUP:
            keyup(event)
