import RPi.GPIO as GPIO
import subprocess 
from gpiozero import Button
import sys

button = Button(17)

def open_dex_and_die(program, exit_code=0):
    # Start the dex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)

button.when_released = open_dex_and_die(['python', 'objectident.py'])













