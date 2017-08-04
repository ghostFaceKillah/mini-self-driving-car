import threading
import subprocess

import lib.constant as cnst

class VlcStreamClient(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        vlc = ['vlc', 'tcp/h264://{}:{}/'.format(self.ip, self.port)]
        subprocess.Popen(vlc)
