import threading

import io
import socket
import struct
import time
import picamera

import lib.constant as cnst

class RpiStreamer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 15

        self.server_address = ('0.0.0.0', port)

        self.server_socket = socket.socket()
        self.server_socket.bind(self.server_address)

    def accept_client(self):
        print('starting up on {}'.format(self.server_address))
        self.sock.listen(1)
        self.connection = server_socket.accept()[0].makefile('wb')

    def run(self):
        self.accept_client()
        try:
            camera.start_recording(connection, format='h264')
            camera.wait_recording(60)
            camera.stop_recording()
        finally:
            connection.close()
            server_socket.close()
