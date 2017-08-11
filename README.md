# mini-self-driving-car
Building a small self driving car


## Stuff to buy
- heat-shrinkable tubes
- radiator for rpi chip?


## Stuff to figure out

#### Goal for now: (Picture, steering) tuple capture software - tested, deployed. Resilent hardware version.

- [ ] improve stability of the video stream
- [ ] upload simplified & corrected schematic of motor control board to this repo (can be done via fritzing)
- [ ] more civilised way to turn off RPI
- [ ] how to make breadboard host for L293 chip more resistant:
    - PCB can be designed using for example [fritzing](fritzing.org)
    - PCBs can be ordered in low quantities from [OSHPark](https://oshpark.com/) (recommended a lot), and [some other places] (https://www.seeedstudio.com/)
- [ ] Make killswitch (turn off engine after 1 second of not streaming of "go forward commands")
- [ ] Correct color coding of the main power line :D


When the above are done, 
- [X] Implement driving system
- [ ] Figure out how to capture testing data        

### DONE (saved here for further motivation)
######  Live wifi-based control from keyboard of GPU computer, very low latency, so driving the car around house is fun
- [X] glue the camera holder in a better way
- [X] Add back gear (wrong wiring on the website!!)
- [X] Reimplement the hardware control with bigger car, as the old one is too small...
- [x] figure out how to power the whole car
- [X] figure out how to stream video over wifi from raspi to gpu computer FAST
- [X] Figure out the picture reading part
- [X] [RPI Camera web interface](http://elinux.org/RPi-Cam-Web-Interface) have reasonable speed to a browser.
           Check how they read data from raspi camera?
- [X] Check what picamera module is actually doing under the hood
- [x] make sure to understand the schematic [here](https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051)      
- [X] Implement steering capture from one computer to another
- [X] How to make steering more reliable? Are we using UDP or sth???
    

## Links and resources found around the web

- https://github.com/hamuchiwa/AutoRCCar

##### Async IO
- https://www.fsl.cs.sunysb.edu/~vass/linux-aio.txt
- http://man7.org/linux/man-pages/man7/aio.7.html
- https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/5/html/Tuning_and_Optimizing_Red_Hat_Enterprise_Linux_for_Oracle_9i_and_10g_Databases/sect-Oracle_9i_and_10g_Tuning_Guide-Enabling_Asynchronous_IO_and_Direct_IO_Support-Verifying_Asynchronous_IO_Usage.html


## Misc useful links

- https://pymotw.com/2/select/
- https://picamera.readthedocs.io/en/release-1.13/
- http://www.scottklement.com/rpg/socktut/nonblocking.html
- https://stackoverflow.com/questions/10654286/why-should-i-use-non-blocking-or-blocking-sockets
- https://stackoverflow.com/questions/1099672/when-is-it-appropriate-to-use-udp-instead-of-tcp

Some person using interesting ultrasound sensor for obstacle detection
- http://www.bajdi.com/obstacle-avoiding-robot-made-from-cheap-parts

Open source breadboard-to-PCB software

http://fritzing.org/home/

How to High power WiFi + RasPi
https://sparkyflight.wordpress.com/2015/07/31/5ghz-wifi-on-the-raspberry-pi-2/

A list of RasPi supported Wifi interfaces
http://elinux.org/RPi_USB_Wi-Fi_Adapters

A guy says one hi-gain interface is good
http://kamilslab.com/2016/01/15/best-5-wifi-adapters-for-the-raspberry-pi-2016/

Nice interactive Raspi Pinout
https://pinout.xyz
