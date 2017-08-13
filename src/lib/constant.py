import os

from definitions import ROOT_DIR

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
# SERVER_IP = '192.168.192.46'
SERVER_IP = '192.168.192.60'

VIDEOS_STREAMING_PORT = 8000
STEERING_PORT = 4567

RASPI_VIDEO_RESOLUTION = (320, 240)
DISPLAY_VIDEO_RESOLUITION = (800, 600)
VIDEO_FRAMERATE = 25
ENCODING = 'utf-8'

MODEL_FILE = os.path.join(ROOT_DIR, 'ml/models/first.json')
WEIGHT_FILE = os.path.join(ROOT_DIR, 'ml/models/first.h5')
