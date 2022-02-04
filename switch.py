import RPi.GPIO as GPIO
import objectident
import subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    input_state = GPIO.input(17)
    if input_state == True:
        exec(open("objectident.py").read())


while False:        
    input_state = GPIO.input(17)
    if input_state == False:
        exit()   
    
       
                   
