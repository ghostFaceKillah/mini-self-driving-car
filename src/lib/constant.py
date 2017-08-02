def msg(direction, action):
    return "{}{}".format(DIRECTION[direction], ACTION[action])

DIRECTION = {
    'up':    'u',
    'down':  'd',
    'right': 'r',
    'left':  'l'
}

REV_DIRECTION = {
    v: k 
    for k, v in DIRECTION.items()
}

ACTION = {
    'start': 'x',
    'stop': 'o'
}

REV_ACTION = {
    v: k 
    for k, v in ACTION.items()
}

RASPI_IP = "192.168.192.42"
SERVER_IP = '192.168.192.60'
VIDEOS_STREAMING_PORT = 8000
KEYBOARD_EVENTS_PORT = 4567

PYGAME_WINDOW_SIZE = (100, 100)
