from pc_steer import PygameDriver
from pc_stream import PygameStreamClient

import pygame

import lib.constant as cnst

pygame.init()
screen = pygame.display.set_mode((640, 480))

driver = PygameDriver(cnst.RASPI_IP, cnst.KEYBOARD_EVENTS_PORT,
                      cnst.PYGAME_WINDOW_SIZE, screen)
stream_client = PygameStreamClient(cnst.RASPI_IP, cnst.VIDEOS_STREAMING_PORT,
                                   screen)

print('Starting driver thread')
driver.start()

print('Starting streaming thread')
stream_client.start()

driver.join()
stream_client.join()
