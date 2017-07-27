# Heavily influenced by github user zhengwang self-driving car project and picamera cookbook

import numpy as np
import cv2
import socket
import matplotlib.pyplot as plt
import tqdm


class VideoStreamingTest(object):
    def __init__(self):
        cv2.startWindowThread()
        cv2.namedWindow('image')

        self.server_socket = socket.socket()
        self.server_socket.bind(('192.168.192.60', 8000))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.streaming()

    def streaming(self):

        try:
            print "Connection from: ", self.client_address
            print "Streaming..."


            stream_bytes = ' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    image = cv2.flip(image, -1)

                    # cv2.imwrite('img/img_{}.png'.format(i), image)
                    cv2.imshow('image', image)
                    # plt.imshow(image)
                    # plt.show()

            print "Done..."

        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    VideoStreamingTest()