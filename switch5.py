import RPi.GPIO as GPIO
from gpiozero import Button
from signal import pause
import subprocess
import sys
## for the LCD screen
import time
import logging
import spidev as SPI
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont
button = Button(17)
#lcd
RST = 0
DC = 0
BL = 0
bus = 0 
device = 0


blankScreen = False
def open_dex_and_die(program, exit_code=0):
    
    # Start the dex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)
    


try:
  
    button.when_released = open_dex_and_die(['python', 'objectident.py'])
    pause()

finally:
    pass

