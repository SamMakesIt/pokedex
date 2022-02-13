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
import spidev as SPI
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont

#thres = 0.45 # Threshold to detect object

# Raspberry Pi pin configuration for the LCD:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 

button = Button(17)                 ## Sets button to 17
cmd_beg= 'sudo espeak '             ## puts sudo espeak in term
cmd_end= ' 2>/dev/null'             ## cleans up the output from the terminal
cmd_voice= '-ven+f4 '               ## Assigns which voice ill be using
homeDir = "/home/pi/Desktop/pokedex/dex"
seen = False                           ##sets seen flag to false 


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
    with open(pokedexFile,"r") as f:
        dexEntry = f.read().rstrip()
    subprocess.call([cmd_beg+cmd_voice+" 'I am a "+dexEntry+"'"+cmd_end], shell=True)
    
## Reopens the button press script killing this process   
def open_button_and_die(program, exit_code=0):
    # Start the dex
    subprocess.Popen(program)
    # close this script
    sys.exit(exit_code)
    
## checks if foundClass is in seen.txt and if not Writes foundClass to seen.txt
def recordFound(seen):
    foundDex = foundClass
    seen = compare(seen)
    recordDex = os.path.abspath("seen.txt")
    with open(recordDex, "a") as f:
        if seen == False:
            f.write(foundDex + "\n")
 
def compare(foundClass):
    if foundClass == open('seen.txt', 'rt').read().split('\n'):
        seen = True
    

def dontRead():
    print('hi')
    
def splashScreen():
    try:
        disp = LCD_2inch4.LCD_2inch4()              ##This block gets the LCD ready
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()

        ## This block pulls and displayes the splash screen
        image = Image.open('/home/pi/Desktop/pokedex/dexGraphics/splashscreen2.jpg')	
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
    
def dexImage():    
    print('nothing is here yet')




## this is getting the video feed
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


  

## this is showing me the output on screen
    while True:
        splashScreen()
        if button.is_pressed: 
            open_button_and_die(['python', 'switch5.py'])
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.60,0.9, objects = ['dog','person'])
        cv2.imshow("Output",result) ##print picture
        cv2.waitKey(1)
           
        for obj in objectInfo:
            foundClass = obj[1]   ##loop through objects identified in picture and speak 
            tts(foundClass)       ## Reads outloud
            compare(foundClass)
            recordFound(foundClass)
           
            
            
            
            
           
            
         
