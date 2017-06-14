# mini-self-driving-car
Building a small self driving car


## Stuff to buy
- heat-shrinkable tubes


## Stuff to figure out

#### Goal for now: Live wifi-based control from keyboard of GPU computer, very low latency, so driving the car around house is fun
- [x] make sure to understand the schematic [here](https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051)
- [ ] upload simplified schematic mentioned above to this repo
- [ ] more civilised way to turn off RPI
- [ ] how to make breadboard host for L293 chip more resistant:
    - [ ] perhaps figure out how to make your own PCB?
- [x] figure out how to power the whole car
- [ ] figure out how to stream video over wifi from raspi to gpu computer FAST
    - [ ] In case of trouble, check how soft for drones is made. Do these guys push live preview of video so fast over cell phone internet?
    - [ ] Figure out the picture reading part
        - [ ] [RPI Camera web interface](http://elinux.org/RPi-Cam-Web-Interface) have reasonable speed to a browser.
             Check how they read data from raspi camera?
        - [ ] Check what picamera module is actually doing under the hood
     - [ ] Figure out the sending part   
        - [ ] read about socketio and eventlet (as used in [here](https://github.com/ghostFaceKillah/behavioral-cloning-self-driving-car/blob/master/drive.py)
        - [ ] read about vanilla py socket module
        - [ ] read about zmq in py
     - [ ] Figure out the displaying part
        - [ ] pygame?
      
    
- [ ] figure out what to figure out


## Links and resources found around the web

- https://picamera.readthedocs.io/en/release-1.10/recipes2.html
- https://github.com/hamuchiwa/AutoRCCar

##### Async IO
- https://www.fsl.cs.sunysb.edu/~vass/linux-aio.txt
- http://man7.org/linux/man-pages/man7/aio.7.html
- https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/5/html/Tuning_and_Optimizing_Red_Hat_Enterprise_Linux_for_Oracle_9i_and_10g_Databases/sect-Oracle_9i_and_10g_Tuning_Guide-Enabling_Asynchronous_IO_and_Direct_IO_Support-Verifying_Asynchronous_IO_Usage.html

##### Raspi cam
- https://github.com/raspberrypi/userland/tree/master/host_applications/linux/apps/raspicam (that's what RPI Cam Web Interface does)
- https://github.com/cedricve/raspicam
- https://github.com/silvanmelchior/RPi_Cam_Web_Interface (the actual RPi Cam web interface repo)
- https://github.com/silvanmelchior/userland/tree/master/host_applications/linux/apps/raspicam (original (??) implementation of raspimjpeg)
- https://github.com/rpicopter/raspimjpeg
- https://github.com/waveform80/picamera



