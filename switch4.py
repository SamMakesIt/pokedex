import RPi.GPIO as GPIO
import time
import subprocess
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
set = 0
while True:
    input_state = GPIO.input(17)
    if input_state == False and set == 0:
        p=subprocess.Popen( "/home/pi/Desktop/pokedex/objectident.py",shell=True,preexec_fn=os.setsid) 
        time.sleep(1)
        set =1
    input_state = GPIO.input(23)
    if input_state == False and set == 1:
        os.killpg(p.pid, signal.SIGTERM)
        time.sleep(1)
        set =0