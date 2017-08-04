"""
A mockup of the actual system.

Questions to be answered:
    1) How is access to state actually handled ? Make an exercise for that.
       Where should be defined the state variable ?
    2) We need timing events (such as send keyboard info update every 100ms)
       Should we syncronize it to a ticking clock? Or maybe we don't care.
       I think syncronisation can be done in general. Look it up.
"""

import pygame
import multiprocessing
import sys

import lib.constant as cnst

state = {
        "image": None, 
        "keyboard_state": {
            "up-down": None,
            "left-right": None
        }
}

state_lock = multiprocessing.Lock()

class ImgGetter(multiprocessing.Process):
    """
    gets the image from pipe, writes it to the state

    def __init__(self, port):
        self.socket()

    def run(self):
        while True:
            data = self.socket.read(xx)
            with lock:
                Update_state()
    """
    pass

class KeyboardSender(multiprocessing.Process):
    """
    sends keboard state to Raspi 10 times per second

    while True:
        with lock:
            keyboard_state = state.keyboard_state
            send_keyboard_state_to_raspi
    """
    pass


class PygameHandler(multiprocessing.Process):
    """
    Process that handles the pygame window update
    and keyboard events. Writes them to state

    1) on keyboard event, update state
    2) update pygame screen at set frequency,
       based on state
    """


    def __init__(self):
        super(PygameHandler, self).__init__()
        pygame.init()
        pygame.display.set_mode((640, 480))
        pass

    def set_keyboard_state(self, direction, action):
        with state_lock:
            print("Updated state")

    def keydown(self, event):
        if event.key == pygame.K_UP:
            self.set_keyboard_state('up', 'start')
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
        print("entering")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    self.keydown(event)
                if event.type == pygame.KEYUP:
                    self.keyup(event)


class StateSaver(multiprocessing.Process):
    """
    orders saving data to the drive at wanted intervals
    Actually it will push data to a queue, from which 
    a set of 3 or so another processes will take data
    and write to the actual drive.

    With frequency xx Hz, check what is in the state
    and put it in the saving queue
    """
    pass


if __name__ == '__main__':

    pygame_handler = PygameHandler()

    pygame_handler.start()
    
    pygame_handler.join()
