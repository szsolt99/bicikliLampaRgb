import RPi.GPIO as GPIO
import time
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

pinFirstOrSecond = 13
pinLightMode = 16
GPIO.setup(pinFirstOrSecond, GPIO.IN)
GPIO.setup(pinLightMode, GPIO.IN)

pinRed = 27
pinGreen = 22
pinBlue = 17
frequency = 60
fill = 100
GPIO.setup(pinRed, GPIO.OUT)
GPIO.setup(pinGreen, GPIO.OUT)
GPIO.setup(pinBlue, GPIO.OUT)
piRed = GPIO.PWM(pinRed, frequency)
piGreen = GPIO.PWM(pinGreen, frequency)
piBlue = GPIO.PWM(pinBlue, frequency)

firstOrSecond = "first"
lightMode = "flicker"

def state():
    print(f"lampa allapota: {firstOrSecond} feny allapota: {lightMode}")
    global fill
    global frequency
    global piRed
    global piGreen
    global piBlue

    piRed.stop()
    piGreen.stop()
    piBlue.stop()
    if firstOrSecond == "first":
        piRed.ChangeFrequency(frequency)
        piRed.ChangeDutyCycle(fill)
        piGreen.ChangeFrequency(frequency)
        piGreen.ChangeDutyCycle(fill)
        piBlue.ChangeFrequency(frequency)
        piBlue.ChangeDutyCycle(fill)
        if lightMode == "flicker":
            piRed.start(fill)
            piGreen.start(fill)
            piBlue.start(fill)
        else:
            piRed.start(fill/3)
            piGreen.start(fill/3)
            piBlue.start(fill/3)

    if firstOrSecond == "second":
        piRed.ChangeDutyCycle(fill)
        piRed.ChangeFrequency(frequency)
        piRed.start(fill)
        

def lampa(channel):
    global firstOrSecond
    if firstOrSecond == "first":
        firstOrSecond = "second"
    elif firstOrSecond == "second":
        firstOrSecond = "first"
    state()

def feny(channel):
    global lightMode
    global fill
    global flicker
    global frequency

    if lightMode == "off":
        lightMode = "static"
        fill = 100
        frequency = 50
        
    elif lightMode == "static":
        lightMode = "flicker"
        frequency = 2
        fill = 50

    elif lightMode == "flicker":
        lightMode = "off"
        fill = 0
        frequency = 50
    state()

GPIO.add_event_detect(pinFirstOrSecond, GPIO.FALLING, callback=feny, bouncetime=500)

GPIO.add_event_detect(pinLightMode, GPIO.FALLING, callback=lampa, bouncetime=500)
feny(1)
state()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("lampa kikapcsolva")
    piRed.stop()
    piGreen.stop()
    piBlue.stop()
    GPIO.cleanup()
    