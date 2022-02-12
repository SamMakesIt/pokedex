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


#thres = 0.45 # Threshold to detect object
button = Button(17)
                 ## Sets button to 17
cmd_beg= 'sudo espeak '             ## puts sudo espeak in term
cmd_end= ' 2>/dev/null'             ## cleans up the output from the terminal
cmd_voice= '-ven+f4 '               ## Assigns which voice ill be using
homeDir = "/home/pi/Desktop/pokedex/dex"

classNames = []                     ## coco.name
classFile = "/home/pi/Desktop/pokedex/coco.names"  ## tells script where names are stored
with open(classFile,"rt") as f:                        
    classNames = f.read().rstrip("\n").split("\n")
configPath = "/home/pi/Desktop/pokedex/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt" #These 2 lines are the object detection DBs
weightsPath = "/home/pi/Desktop/pokedex/frozen_inference_graph.pb"
## pokedex entries file
#dexEntry = []
#pokedexFile =  "'/home/pi/Desktop/pokedex/'foundClass.txt"
#with open(pokedexFile,"rt") as f:
    #dexEntry = f.read().rstrip("\n").split("\n")
    


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
    
def recordFound(recordDex):
    recordDex = os.path.abspath("seen.txt")
    with open(recordDex, "a") as f:
        f.write(foundClass + "\n")
 

def dontRead():
    print('hi')
    


## this is getting the video feed
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    

## this is showing me the output on screen
    while True:
        
        if button.is_pressed: 
            open_button_and_die(['python', 'switch5.py'])    
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.60,0.9, objects = ['dog','person'])
        cv2.imshow("Output",result) ##print picture
        cv2.waitKey(1)
           
        for obj in objectInfo:
            foundClass = obj[1]   ##loop through objects identified in picture and speak 
            tts(foundClass)       ## Reads outloud
            recordFound(foundClass)
           
            
            
            
            
           
            
         
