# Heavily influenced by github user zhengwang self-driving car project and picamera cookbook

import numpy as np
import cv2
import socket
import matplotlib.pyplot as plt
import tqdm


cv2.startWindowThread()
cv2.namedWindow('image')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('192.168.192.60', 8000))

try:
    stream_bytes = ' '
    while True:
        image = None
        print "Trying to parse image"
        data = server_socket.recv(131072)
        stream_bytes += data
        first = stream_bytes.find('\xff\xd8')
        last = stream_bytes.find('\xff\xd9')
        if first != -1 and last != -1:
            jpg = stream_bytes[first:last + 2]
            stream_bytes = stream_bytes[last + 2:]
            image = cv2.imdecode(
                np.fromstring(jpg, dtype=np.uint8),
                cv2.IMREAD_UNCHANGED
            )
            image = cv2.flip(image, -1)

            cv2.imshow('image', image)

finally:
    server_socket.close()
