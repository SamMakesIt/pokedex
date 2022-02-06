import RPi.GPIO as GPIO
import objectident
import subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
state = GPIO.input(17)

while True:
    
    if state == True:
        print('camera is on')
        exec(open("objectident.py").read())
        break
    elif state == False:
        print('camera is off')
        
