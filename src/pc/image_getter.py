import threading
import subprocess
import socket
import cv2
import numpy as np

import lib.constant as cnst


class VideoStreamClient(threading.Thread):
    """
    Gets the image from the wire, writes it to the state.
    """
    def __init__(self, the_state):
        threading.Thread.__init__(self)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', cnst.VIDEOS_STREAMING_PORT))
        self.state = the_state

    def parse_image(self, stream_bytes, first, last):
        """ Parse an image from data in the byte stream """
        jpg = stream_bytes[first:last + 2]
        image = cv2.imdecode(
            np.fromstring(jpg, dtype=np.uint8),
            cv2.IMREAD_UNCHANGED
        )

        image = cv2.flip(image, -1)
        image = np.transpose(image, axes=(1, 0, 2))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.state.image = image

    def run(self):
        # TODO(all): Refactor!
        try:
            stream_bytes = b' '
            while True:
                # Read data from wire
                data = self.sock.recv(131072)
                stream_bytes += data

                # Try to interpret stream as jpeg
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    self.parse_image(stream_bytes, first, last)
                    stream_bytes = stream_bytes[last + 2:]

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
