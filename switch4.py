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


button1 = Button()
button2 = Button()
#lcd
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0


def open_dex_and_die(program, exit_code=0):
    
    # Start the dex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)
    
def cycle_dex()
    try:
        disp = LCD_2inch4.LCD_2inch4()              ##This block gets the LCD ready
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()

        
        dexImage = os.path.abspath("dexGraphics/dexEntryGraphics/")
        seenFile = os.path.abspath("seen/")
        if os.path.isfile(seenFile) = dexImage:
                        
        ## This block pulls and display the dex entry
            image = Image.open("/home/pi/Desktop/pokedex/dexGraphics/dexEntryGraphics/"+ foundClass +'.jpg')
            image = image.rotate(0)
            disp.ShowImage(image)
            time.sleep(3)
            disp.module_exit()
    
    except IOError as e:
        logging.info(e)    
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()
    
    
try:
    button.when_pressed = open_dex_and_die(['python', 'objectident.py'])
    pause()

finally:
    pass
