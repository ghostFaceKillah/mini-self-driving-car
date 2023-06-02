# mini-self-driving-car

[Read the write-up here!](https://ghostfacekillah.github.io/car.html)

Building a small self driving car!

* [Stuff to do](stuff-to-do)
* [Done](done)
* [Links an resources](links-and-resources-found-around-the-web)
* [Misc tips](misc-tips)
* [Usage](usage)
  - [Heat map](heat-map)


## Stuff to do

#### GOAL: Implement good quality loop around a bigger track.

For the above goal better steering seems really necessary


##### Software
- [ ] Improve the quality of code:
   - Comment
   - General code quality (read through and think)
   - Abstract socket
   - Catch typical unhandled exceptions on Raspi side
   - Catch typical unhandled exceptions on PC side


##### Machine learning
- [ ] Gather a lot of data
- [ ] Build good model


##### Hardware
- [ ] Make steering better, perhaps add the proper L293D wiring or consider making a better car with PWM steering.

- [ ] Attach the pi camera in a sturdy way
- [ ] more civilised way to turn off RPI
- [ ] Make killswitch (turn off engine after 1 second of not streaming of "go forward commands")
- [ ] Correct color coding of the main power line :D
- [ ] Add some caps to the motor controller like [here] (http://www.instructables.com/id/Control-your-motors-with-L293D-and-Arduino/), explained [here](https://robotics.stackexchange.com/questions/267/why-are-capacitors-added-to-motors-in-parallel-what-is-their-purpose)


##### Misc
 - [ ] Start preparing write up and tutorial for the sake of posterity
 - [ ] upload simplified & corrected schematic of motor control board to this repo (can be done via fritzing)


## DONE (saved here for further motivation)

#### Big goals:
- ######  Live wifi-based control from keyboard of GPU computer, very low latency, so driving the car around house is fun
- ######  (Picture, steering) tuple capture software - tested, deployed! Kind of OK hardware version!
- ######  Implement and test a self-driven 1 turn

#### Smaller goals:


##### Machine learning
- [X] Add dataset merging capability
- [X] Gather more data and train first serious model run
- [X] Implement data augmentation
- [X] Add capability to load model and run on one image to check how it works
- [X] See how well the first model performs - bad ! (but in night lighting)


- [X] improve stability of the video stream
- [X] Implement driving system
- [X] Figure out how to capture testing data        
- [X] glue the camera holder in a better way
- [X] Add back gear (wrong wiring on the website!!)
- [X] Reimplement the hardware control with bigger car, as the old one is too small...
- [x] figure out how to power the whole car
- [X] figure out how to stream video over wifi from raspi to gpu computer FAST
- [X] Figure out the picture reading part
- [X] [RPI Camera web interface](http://elinux.org/RPi-Cam-Web-Interface) have reasonable speed to a browser.
           Check how they read data from raspi camera?
- [X] make breadboard host for L293 chip more resistant (we have decided to ignore it, as current breadboard is resillent enough):
    - PCB can be designed using for example [fritzing](fritzing.org)
    - PCBs can be ordered in low quantities from [OSHPark](https://oshpark.com/) (recommended a lot), and [some other places] (https://www.seeedstudio.com/)
- [X] Check what picamera module is actually doing under the hood
- [x] make sure to understand the schematic [here](https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051)      
- [X] Implement steering capture from one computer to another
- [X] How to make steering more reliable? Are we using UDP or sth???
    

## Links and resources found around the web

There are many, many people doing similar stuff

- https://github.com/hamuchiwa/AutoRCCar
- https://www.raspberrypi.org/magpi/self-driving-rc-car/
- https://github.com/wroscoe/donkey
- https://diyrobocars.com (autonomous RC car racing)
- http://blog.davidsingleton.org/nnrccar/

Also in pretty high quality, using a lot of expensive stuff:
- https://github.com/mit-racecar

###### Async IO
- https://www.fsl.cs.sunysb.edu/~vass/linux-aio.txt
- http://man7.org/linux/man-pages/man7/aio.7.html
- https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/5/html/Tuning_and_Optimizing_Red_Hat_Enterprise_Linux_for_Oracle_9i_and_10g_Databases/sect-Oracle_9i_and_10g_Tuning_Guide-Enabling_Asynchronous_IO_and_Direct_IO_Support-Verifying_Asynchronous_IO_Usage.html


###### Sending data over ether

- https://pymotw.com/2/select/
- https://picamera.readthedocs.io/en/release-1.13/
- http://www.scottklement.com/rpg/socktut/nonblocking.html
- https://stackoverflow.com/questions/10654286/why-should-i-use-non-blocking-or-blocking-sockets
- https://stackoverflow.com/questions/1099672/when-is-it-appropriate-to-use-udp-instead-of-tcp

Some person using interesting ultrasound sensor for obstacle detection
- http://www.bajdi.com/obstacle-avoiding-robot-made-from-cheap-parts

Open source breadboard-to-PCB software
- http://fritzing.org/home/

High quality MIT copy of this project
- https://beaverworks.ll.mit.edu/CMS/bw/bwsi-mgpc

How to High power WiFi + RasPi
- https://sparkyflight.wordpress.com/2015/07/31/5ghz-wifi-on-the-raspberry-pi-2/

Lists of RasPi supported Wifi interfaces
- http://elinux.org/RPi_USB_Wi-Fi_Adapters
- http://kamilslab.com/2016/01/15/best-5-wifi-adapters-for-the-raspberry-pi-2016/

Nice interactive Raspi Pinout
https://pinout.xyz

Some discussion what can burn L293D
http://forum.arduino.cc/index.php?topic=16328.0


## Misc tips

How to quickly kill a process using port 8000 in Linux?

```
fuser -k 8000/udp
```

## Usage
All scripts should be invoked from the `src` directory.
### Heat map
```
usage: heatmap.py [-h] image_path layer_no feature_maps [feature_maps ...]

positional arguments:
  image_path    path to image to view heatmap of
  layer_no      number of layer to stop the computation on
  feature_maps  number of feature map to display

optional arguments:
  -h, --help    show this help message and exit
```
