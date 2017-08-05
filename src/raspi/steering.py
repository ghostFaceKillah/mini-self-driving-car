import socket
import multiprocessing

import lib.constant as cnst
import gpio

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('0.0.0.0', cnst.STEERING_PORT)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)


def interpret(msg):
    direction = cnst.REV_DIRECTION[msg[0]]
    action = cnst.REV_ACTION[msg[1]]

    if direction == 'up':
        if action == 'start':
            gpio.go_forward()
        elif action == 'stop':
            gpio.stop()

    elif direction == 'down':
        if action == 'start':
            gpio.go_back()
        elif action == 'stop':
            gpio.stop()

    elif direction == 'right':
        if action == 'start':
            gpio.turn_right()
        elif action == 'stop':
            gpio.stop_turning()

    elif direction == 'left':
        if action == 'start':
            gpio.turn_left()
        elif action == 'stop':
            gpio.stop_turning()


class Steering(multiprocessing.Process):

    def run(self):
        try:
            gpio.init()
            while True:
                data, client_address = sock.recvfrom(16)

                print 'received {} from {}'.format(data, client_address)
                interpret(data)

        finally:
            gpio.clean_up()
