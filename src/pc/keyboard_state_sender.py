import multiprocessing
import socket
import time

import lib.constant as cnst
import lib.state as state


class KeyboardSender(multiprocessing.Process):
    """
    sends keboard state to Raspi 10 times per second

    while True:
        with lock:
            keyboard_state = state.keyboard_state
            send_keyboard_state_to_raspi
    """
    def __init__(self, the_state):
        super(KeyboardSender, self).__init__()
        self.state = the_state

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, msg):
        self.sock.sendto(
            bytes(msg, encoding=cnst.ENCODING),
            (cnst.RASPI_IP, cnst.STEERING_PORT)
        )

    def run(self):
        while True:
            time.sleep(0.1)

            # Send direction state
            if self.state.horizontal == state.Horizontal.left:
                msg = cnst.msg('left', 'start')
            elif self.state.horizontal == state.Horizontal.right:
                msg = cnst.msg('right', 'start')
            else:
                msg = cnst.msg('right', 'stop')

            self.send(msg)

            # Send start stop msg
            if self.state.vertical ==  state.Vertical.up:
                msg = cnst.msg('up', 'start')
            elif self.state.vertical ==  state.Vertical.down:
                msg = cnst.msg('down', 'start')
            else:
                msg = cnst.msg('up', 'stop')

            self.send(msg)
