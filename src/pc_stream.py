import threading
import subprocess
import socket
import pygame
import cv2
import numpy as np

import lib.constant as cnst

class PygameStreamClient(threading.Thread):
    def __init__(self, ip, port, pg_screen):
        threading.Thread.__init__(self)
        self.server_ip = ip
        self.server_port = port
        self.screen = pg_screen

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.server_ip, self.server_port))

    def run(self):
        self.connect()
        try:
            stream_bytes = b' '
            while True:
                image = None
                print("Trying to parse image")
                data = self.sock.recv(131072)
                stream_bytes += data
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    npjpg = np.fromstring(jpg, dtype=np.uint8)
                    image = cv2.imdecode(
                        np.fromstring(jpg, dtype=np.uint8),
                        cv2.IMREAD_UNCHANGED
                    )
                    image = cv2.flip(image, -1)
                    pimage = pygame.image.fromstring(image.tostring(), image.shape[1::-1], "RGB")
                    self.screen.blit(pimage, (0, 0))

                    pygame.display.flip()
        
                    #  cv2.imshow('image', image)
        
        finally:
            self.sock.close()

class VlcStreamClient(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        cv2.startWindowThread()
        cv2.namedWindow('image')


    def run(self):
        vlc = ['vlc', 'tcp/h264://{}:{}/'.format(self.ip, self.port)]
        subprocess.Popen(vlc)
