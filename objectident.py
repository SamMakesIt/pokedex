## object identification module 
import cv2
##Lets tts say numbers
from num2words import num2words
##subprocess opens a terminal to run tts commands 
from subprocess import call

#thres = 0.45 # Threshold to detect object

cmd_beg= 'sudo espeak '             ## puts sudo espeak in term
cmd_end= ' 2>/dev/null'                ## cleans up the output from the terminal
cmd_voice= '-ven+f4 '               ## Assigns which voice ill be using
classNames = []                     ## coco.name
#call([cmd_beg+text+cmd_end] shell=True)
cv2Text = cv2.putText                           ##
cv2.putText = classNames[classId - 1].upper()  ## not sure if this is right tbth
classNames = classId                            ##
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
def getObjects(img, thres, nms, draw=True, objects=[]):
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

## this is the test function for TTS im lost here tbth
def tts():
    if cv2Text == 'DOG':
        call([cmd_beg+cmd_voice+" I+am+a+dog"+cmd_end], shell=True)
    if cv2Text == 'PERSON':
        call([cmd_beg+cmd_voice+" I+am+a+person"+cmd_end], shell=True)


## this is getting the video feed
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)

## this is showing me the output on screen
    while True:
            success, img = cap.read()
            result, objectInfo = getObjects(img,0.65,0.6, objects=['dog','person']), tts
            #print(objectInfo)
            cv2.imshow("Output",img)
            cv2.waitKey(1)
            
            
           
            
         
