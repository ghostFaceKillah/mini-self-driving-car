import lib.state as st
import pygame


class PygameHandler(multiprocessing.Process):
    """
    Process that handles the pygame window update
    and keyboard events. Writes them to state

    1) on keyboard event, update state
    2) update pygame screen at set frequency,
       based on state

    import cv2
    import ipdb
    import numpy as np
    import pygame
    import time

    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    img = cv2.imread('example.jpg')
    img = np.transpose(img, axes=(1, 0, 2))

    screen.blit(pygame.surfarray.make_surface(img), (0, 0))
    pygame.display.flip()


    while True:
    time.sleep(0.2)

    """

    def __init__(self, state):
        super(PygameHandler, self).__init__()

        pygame.init()
        pygame.display.set_mode((640, 480))

        self.state = state


    def set_keyboard_state(self, direction, value):
        with self.state[st.StatePart.lock]:
            self.state[st.StatePart.keyboard][direction] = value


    def keydown(self, event):
        if event.key == pygame.K_UP:
            self.set_keyboard_state(
                'up_down', 'start'
            )
        if event.key == pygame.K_DOWN:
            self.set_keyboard_state('down', 'start')
        if event.key == pygame.K_RIGHT:
            self.set_keyboard_state('right', 'start')
        if event.key == pygame.K_LEFT:
            self.set_keyboard_state('left', 'start')

    def keyup(self, event):
        if event.key == pygame.K_UP:
            self.set_keyboard_state('up', 'stop')
        if event.key == pygame.K_DOWN:
            self.set_keyboard_state('down', 'stop')
        if event.key == pygame.K_RIGHT:
            self.set_keyboard_state('right', 'stop')
        if event.key == pygame.K_LEFT:
            self.set_keyboard_state('left', 'stop')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    self.keydown(event)
                if event.type == pygame.KEYUP:
                    self.keyup(event)
