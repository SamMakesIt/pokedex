## object identification module 
import cv2
##Lets tts say numbers
from num2words import num2words
##subprocess opens a terminal to run tts commands 
import subprocess
import os
#Imports button controll
from gpiozero import Button
import sys
## for the LCD screen
import time
import logging
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont
import glob
import spidev as SPI


#thres = 0.45 # Threshold to detect object

# Raspberry Pi pin configuration for the LCD:
RST = 27
DC = 25
BL = 6
bus = 0 
device = 0


button1 = Button(17)                ## Sets button to 17
#button2 = Button(16)
button3 = Button(22)
cmd_beg= 'sudo espeak -s160 '             ## puts sudo espeak in term
cmd_end= ' 2>/dev/null'             ## cleans up the output from the terminal
cmd_voice= '-ven+m5 '               ## Assigns which voice ill be using
homeDir = "/home/pi/Desktop/pokedex/dex"
splashRan = False

classNames = []                     ## coco.name
classFile = "/home/pi/Desktop/pokedex/coco.names"  ## tells script where names are stored
with open(classFile,"rt") as f:                        
    classNames = f.read().rstrip("\n").split("\n")
configPath = "/home/pi/Desktop/pokedex/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt" #These 2 lines are the object detection DBs
weightsPath = "/home/pi/Desktop/pokedex/frozen_inference_graph.pb"

    
## this is more standard detection stuff
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

##this is the meat of the detection, tells it how to draw the box, and to label inside the box
def getObjects(img, thres, nms, draw=True, objects=[],):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    
                    

    return img,objectInfo

## this is the text to speech function. it calls the dex entries from /dex and reads the file
def tts(dexEntry):
    pokedexFile = os.path.abspath("dex/" + foundClass +'.txt')
    seenFile = os.path.abspath("seen/" + foundClass +'.txt')
    if os.path.isfile(seenFile):
        pass
    else:
        with open(pokedexFile,"r") as f:
            dexEntry = f.read().rstrip()
        subprocess.call([cmd_beg+cmd_voice+dexEntry+cmd_end], shell=True)
    
## Reopens the button press script killing this process   
def open_switch_and_die(program, exit_code=0):
    # Start the dex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)
    
def open_seenDex_and_die(program, exit_code=0):
    # open seenDex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)
    
def delete_seen():
    # Start the dex
    dir = '/home/pi/Desktop/pokedex/seen'
    for file in os.scandir(dir):
        os.remove(file.path)
    
## checks if foundClass is in seen.txt and if not Writes foundClass to seen.txt
def recordFound(fileFound):
    seenFile = os.path.abspath("seen/" + foundClass +'.txt')
    if os.path.isfile(seenFile):
        pass
    else:
        f = open(seenFile, "w")
        f.close()
    
   
def splashScreen():
    
    
    disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)              ##This block gets the LCD ready
        # Initialize library.
    disp.Init()
        # Clear display.
    disp.clear()
        
        
    
    image = Image.open('/home/pi/Desktop/pokedex/dexGraphics/splashscreen2.jpg')	
    image = image.rotate(0)
    disp.ShowImage(image)
    time.sleep(3)
    disp.module_exit()
    
   
def dexImage(foundClass):    
    

    disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)              ##This block gets the LCD ready
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    seenFile = os.path.abspath("seen/" + foundClass +'.txt')

    if os.path.isfile(seenFile):
        pass
    else:
        image = Image.open("/home/pi/Desktop/pokedex/dexGraphics/dexEntryGraphics/"+ foundClass +'.jpg')
        image = image.rotate(0)
        disp.ShowImage(image)
        time.sleep(3)
        disp.module_exit()



## this is getting the video feed
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


  

## this is showing me the output on screen
    while True:
        
        
        
        if splashRan == False:
            splashScreen()
            splashRan = True
        if button1.is_pressed: 
            open_switch_and_die(['python', 'switch5.py'])
        #if button2.is_pressed: 
           # open_switch_and_die(['python', 'switch4.py'])
        if button3.is_pressed:
            delete_seen()
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.60,0.9, objects = ['dog','person'])
        cv2.imshow("Output",result) ##print picture
        cv2.waitKey(1)
          
        for obj in objectInfo:
            foundClass = obj[1]   ##loop through objects identified in picture and speak  
            seenFile = os.path.abspath("seen/" + foundClass +'.txt')
            if os.path.isfile(seenFile):
                pass
            else:
                dexImage(foundClass)
                splashRan = False
                tts(foundClass)       ## Reads outloud
                recordFound(foundClass)
            
            
            
            
            
           
            
         
