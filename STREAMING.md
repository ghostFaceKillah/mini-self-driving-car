
## Raspivid method

A method suggested [here](https://raspberrypi.stackexchange.com/questions/27082/how-to-stream-raspivid-to-linux-and-osx-using-gstreamer-vlc-or-netcat) works very nice.

On client
```
nc -l 2222 | mplayer -fps 200 -demuxer h264es -
```

On raspi
```
raspivid -t 0 -w 300 -h 300 -vf -fps 20 -o - | nc <client-ip> 2222
```

Raspivid source:
https://github.com/raspberrypi/userland/blob/master/host_applications/linux/apps/raspicam/RaspiVid.c



## picamera method

used in at least 3 known places:
- Wang Zheng implementation
- [picamera easy recipe](https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-to-a-network-stream)
- [picamera advanced recipe](https://picamera.readthedocs.io/en/release-1.13/recipes2.html#rapid-capture-and-streaming)

I have tested the advanced implementation from above. It looks like it will be sufficient for now. around 30 ms latency.



## Random links

- [ ] Figure out the sending part   
  - [ ] read about socketio and eventlet (as used in [here](https://github.com/ghostFaceKillah/behavioral-cloning-self-driving-car/blob/master/drive.py)
  - [ ] read about vanilla py socket module
  - [ ] read about zmq in py
  - [ ] read about io package in python as used [here](https://picamera.readthedocs.io/en/release-1.13/recipes2.html#rapid-capture-and-streaming)
        

##### Raspi cam
- https://github.com/raspberrypi/userland/tree/master/host_applications/linux/apps/raspicam (that's what RPI Cam Web Interface does)
- https://github.com/cedricve/raspicam
- https://github.com/silvanmelchior/RPi_Cam_Web_Interface (the actual RPi Cam web interface repo)
- https://github.com/silvanmelchior/userland/tree/master/host_applications/linux/apps/raspicam (original (??) implementation of raspimjpeg)
- https://github.com/rpicopter/raspimjpeg
- https://github.com/waveform80/picamera

