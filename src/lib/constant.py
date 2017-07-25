DIRECTION = {
    'up':    'u',
    'down':  'd',
    'right': 'r',
    'left':  'l'
}

REV_DIRECTION = {
    v: k 
    for k, v in DIRECTION.iteritems()
}

ACTION = {
    'start': 'x',
    'stop': 'o'
}

REV_ACTION = {
    v: k 
    for k, v in ACTION.iteritems()
}

RASPI_IP = "192.168.192.51"
KEYBOARD_EVENTS_PORT = 4567
