"""
A mockup of the actual system.

Questions to be answered:
    1) How is access to state actually handled ? Make an exercise for that.
       Where should be defined the state variable ?
    2) We need timing events (such as send keyboard info update every 100ms)
       Should we syncronize it to a ticking clock? Or maybe we don't care.
       I think syncronisation can be done in general. Look it up.
"""

import multiprocessing

state = {
        "image": img,
        "keyboard_state": {
            "up-down": None,
            "left-right": None
        }
}

class ImgGetter(multiprocessing.Process):
    """
    gets the image from pipe, writes it to the state
    """
    def __init__(self, port):
        self.socket()

    def run(self):
        while True:
            data = self.socket.read(xx)
            with lock:
                Update_state()


class KeyboardSender(multiprocessing.Process):
    """
    sends keboard state to Raspi 10 times per second
    """

    while True:
        with lock:
            keyboard_state = state.keyboard_state
            send_keyboard_state_to_raspi


class PygameHandler(multiprocessing.Process):
    """
    Process that handles the pygame window update
    and keyboard events. Writes them to state
    """

    1) on keyboard event, update state
    2) update pygame screen at set frequency,
       based on state


class StateSaver(multiprocessing.Process):
    """
    orders saving data to the drive at wanted intervals
    Actually it will push data to a queue, from which 
    a set of 3 or so another processes will take data
    and write to the actual drive.
    """

    With frequency xx Hz, check what is in the state
    and put it in the saving queue
