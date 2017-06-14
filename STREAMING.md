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


