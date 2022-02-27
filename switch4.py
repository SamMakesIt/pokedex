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
button1 = Button(2)
button2 = Button(22)
button3 = Button(16)
#lcd
RST = 27
DC = 25
BL = 6
bus = 0 
device = 0
seenFileName = '/home/pi/seen/'
fileNames = [os.path.splitext(filename)[0] for filename in os.listdir(seenFileName)]
index = 0
dexEntryAmt = len(fileNames)


def open_dex_and_die(program, exit_code=0):
    
    # Start the dex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)
   
def showDex():
    
    disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL) 
    #disp = LCD_2inch4.LCD_2inch4()              ##This block gets the LCD ready
        # Initialize library.
    disp.Init()
        # Clear display.
    disp.clear()

        
    dexImage = os.path.abspath("dexGraphics/dexEntryGraphics/")
        
        
                
                        
        ## This block pulls and display the dex entry
    image = Image.open("/home/pi/dexGraphics/dexEntryGraphics/"+fileNames[index]+'.jpg')
    image = image.rotate(0)
    disp.ShowImage(image)
    time.sleep(1)
    disp.module_exit()
    

  
if dexEntryAmt > 0:   
    showDex()
else:                          ##You need to see more things lvl 0 scrub. . . git gud!
    open_dex_and_die(['python', 'objectident.py'])
while dexEntryAmt > 0:    
    
    
    
    if button1.is_pressed: 
        index = (index + 1) % dexEntryAmt
        showDex()
        print(index)        
        
    if button2.is_pressed:
        index = (index - 1) % dexEntryAmt
        showDex()
        print(index)
        
        
    if button3.is_pressed:
        open_dex_and_die(['python', 'objectident.py'])
        
    



