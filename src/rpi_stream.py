import threading

import io
import socket
import struct
import time
import picamera

class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

class PiStreamer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('0.0.0.0', port)
        self.sock.bind(self.server_address)

    def wait_for_client(self):
        print('starting up on {}'.format(self.server_address))
        self.sock.listen(1)

        self.client_socket, self.client_address = self.sock.accept()
        self.connection = self.client_socket.makefile('wb')

    def run(self):
        self.wait_for_client()
        try:
            output = SplitFrames(self.connection)
            with picamera.PiCamera(resolution=(640, 480), framerate=25) as camera:
                time.sleep(2)
                camera.start_recording(output, format='mjpeg')
                camera.wait_recording(6000)
                camera.stop_recording()
        finally:
            self.client_socket.close()
