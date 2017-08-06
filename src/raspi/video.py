import socket
import time
import picamera

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(('192.168.192.60', 8000))
connection = client_socket.makefile('wb')

while True:
    try:
        with picamera.PiCamera(resolution=(320, 240), framerate=25) as camera:
            time.sleep(2)
            start = time.time()
            camera.start_recording(connection, format='mjpeg')
            camera.wait_recording(6000)
            camera.stop_recording()

    finally:
        client_socket.close()
        time.sleep(1.0)

