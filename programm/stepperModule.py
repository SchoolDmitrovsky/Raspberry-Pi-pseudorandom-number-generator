import RPi.GPIO as GPIO
import time

dirPin = 20
stepPin = 21
btnPin = 16

dirPin2 = 9
stepPin2 = 11
btnPin2 = 19

btnPin3 = 13

btnPin4 = 6

pos = 0
pos2 = 0

spr = 200 #steps per revolution
microstep = 16
ppr = spr * microstep #pulses per revolution

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin, GPIO.OUT)

GPIO.setup(dirPin2, GPIO.OUT)
GPIO.setup(stepPin2, GPIO.OUT)

GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnPin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def goTo(newPos):
    global pos
    while pos != newPos:        
        direction = pos < newPos
        GPIO.output(dirPin, direction)
        
        if direction:
            pos += 1
        else:
            pos -= 1
        GPIO.output(stepPin, pos % 2)
        time.sleep(0.0003)

def goTo2(newPos):
    global pos2
    while pos2 != newPos:        
        direction = pos2 < newPos
        GPIO.output(dirPin2, direction)
        
        if direction:
            pos2 += 1
        else:
            pos2 -= 1
        GPIO.output(stepPin2, pos2 % 2)
        time.sleep(0.00015)
        
def baraban():
    goTo(32000)
    time.sleep(1)
    goTo(32000-3200)
    time.sleep(1)
    goTo(32000)
    time.sleep(1)
    pos = 0

def lift():
    goTo2(49500)
    time.sleep(1)
    goTo2(43000)
    time.sleep(.5)
    goTo2(0)
    time.sleep(1)
    pos2 = 0

try:
    while True:
        if not GPIO.input(btnPin):
            baraban()
            
        if not GPIO.input(btnPin2):
            lift()
            
        if not GPIO.input(btnPin3):
            goTo2(10000)
            file = open('kameraModule.py','r')
            exec(file.read())
        if not GPIO.input(btnPin4):
            while True:
                baraban()
                time.sleep(1)
                goTo2(10000)
                file = open('kameraModule.py','r')
                exec(file.read())
                time.sleep(1)
                lift()
                time.sleep(1)
            
        
        
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
