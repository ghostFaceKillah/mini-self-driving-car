import multiprocessing
import picamera
import socket
import time

import lib.constant as cnst


class VideoStreaming(multiprocessing.Process):

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.connect((cnst.SERVER_IP, cnst.VIDEOS_STREAMING_PORT))
        connection = client_socket.makefile('wb')

        try:
            opts = dict(
                resolution=cnst.VIDEO_RESOLUTION,
                framerate=cnst.VIDEO_FRAMERATE
            )

            with picamera.PiCamera(**opts) as camera:
                time.sleep(2)
                camera.start_recording(connection, format='mjpeg')
                camera.wait_recording(60000)
                camera.stop_recording()

        finally:
            client_socket.close()

