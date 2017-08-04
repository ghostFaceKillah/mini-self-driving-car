"""
A mockup of the actual system.

Questions to be answered:
    1) How is access to state actually handled ? Make an exercise for that.
       Where should be defined the state variable ?
    2) We need timing events (such as send keyboard info update every 100ms)
       Should we syncronize it to a ticking clock? Or maybe we don't care.
       I think syncronisation can be done in general. Look it up.
"""

import enum
import pygame
import multiprocessing
import sys

import lib.constant as cnst
import lib.state as state

from pc.pygame_handler import PygameHandler

the_state = {
    state.StatePart.lock: None,
    state.StatePart.image: None,
    state.StatePart.keyboard: {
        state.Direction.up_down: None,
        state.Direction.left_right: None
    }
}

state_lock = multiprocessing.Lock()



if __name__ == '__main__':
    pygame_handler = PygameHandler()
    pygame_handler.start()
    pygame_handler.join()
