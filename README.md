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
