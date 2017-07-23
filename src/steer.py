import RPi.GPIO as GPIO
from time import sleep
import keyboard

GPIO.setmode(GPIO.BOARD)

Motor1A = 36  # 16
Motor1B = 38  # 18
Motor1E = 40  # 22

Motor2A = 37  # 23
Motor2B = 35  # 21
Motor2E = 33  # 19

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

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


def stop():
    print "Stopping the car"
    GPIO.output(Motor2E, GPIO.LOW)


def register_hooks():
    print "Registering hooks"
    keyboard.hook_key('up', keydown_callback=go_forward, keyup_callback=stop)
    keyboard.hook_key('left', keydown_callback=turn_left, keyup_callback=stop_turning)
    keyboard.hook_key('right', keydown_callback=turn_right, keyup_callback=stop_turning)
    print "Hooks registered"


if __name__ == '__main__':
    try:
        register_hooks()
        stop()
        stop_turning()
        while True:
            sleep(0.1)
    finally:
        print "Clean up"
        GPIO.cleanup()
