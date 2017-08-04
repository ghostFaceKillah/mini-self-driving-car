import multiprocessing
import picamera
import socket
import time


def stream():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect(('192.168.192.60', 8000))
    connection = client_socket.makefile('wb')

    try:
        with picamera.PiCamera(resolution=(640, 480), framerate=25) as camera:
            time.sleep(2)
            camera.start_recording(connection, format='mjpeg')
            camera.wait_recording(60000)
            camera.stop_recording()

    finally:
        client_socket.close()



VideoStreaming = multiprocessing.Process(target=stream)
