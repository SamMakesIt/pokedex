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
from pathlib import Path
import os
from pathlib import Path
from os.path import isfile, join
from os import listdir
button1 = Button(17)
button2 = Button(22)
button3 = Button(16)
#lcd
RST = 27
DC = 25
BL = 6
bus = 0 
device = 0
seenFileName = '/home/pi/Desktop/pokedex/seen/'
storeFileName = files = [os.path.splitext(filename)[0] for filename in os.listdir(seenFileName)]
fileNames = storeFileName

def open_dex_and_die(program, exit_code=0):
    
    # Start the dex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)
   
def cycle_dex():
    
    disp = LCD_2inch4.LCD_2inch4()              ##This block gets the LCD ready
        # Initialize library.
    disp.Init()
        # Clear display.
    disp.clear()

        
    dexImage = os.path.abspath("dexGraphics/dexEntryGraphics/")
        
        
                
                        
        ## This block pulls and display the dex entry
    image = Image.open("/home/pi/Desktop/pokedex/dexGraphics/dexEntryGraphics/"+ foundClass +'.jpg')
    image = image.rotate(0)
    disp.ShowImage(image)
    time.sleep(3)
    disp.module_exit()
    
    
    
    
try:
    for button1.when_pressed:
        
    button3.when_pressed = open_dex_and_die(['python', 'objectident.py'])
    pause()

finally:
    pass



