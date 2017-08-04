import RPi.GPIO as GPIO


Motor1A = 33
Motor1B = 35
Motor1E = 37

Motor2A = 38
Motor2B = 40
Motor2E = 36

GPIO.setmode(GPIO.BOARD)


def turn_right():
    print "Turning the steering right"
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)

def stop_turning():
    print "Stopping motor"
    GPIO.output(Motor1E, GPIO.LOW)


def turn_left():
    print "Turning the steering left"
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)


def go_forward():
    print "Going forward"
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)


def go_back():
    print "Going back"
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    GPIO.output(Motor2E, GPIO.HIGH)


def stop():
    print "Stopping the car"
    GPIO.output(Motor2E, GPIO.LOW)


def init():
    GPIO.setup(Motor1A, GPIO.OUT)
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)

    GPIO.setup(Motor2A, GPIO.OUT)
    GPIO.setup(Motor2B, GPIO.OUT)
    GPIO.setup(Motor2E, GPIO.OUT)

    stop()
    stop_turning()


def clean_up():
    print "Cleaning up GPIO"
    GPIO.cleanup()
