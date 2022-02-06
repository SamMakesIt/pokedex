import RPi.GPIO as GPIO
import time
import subprocess, os
import signal
import objectident

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_switch = 17  # pin 17
GPIO.setup(GPIO_switch,GPIO.IN)



try:
    
   run = False
   while True :
      if GPIO.input(GPIO_switch)==False and run == False:
         print ("  Started")
         exec(open("objectident.py").read())
         run = True
         while GPIO.input(GPIO_switch)==0:
             time.sleep(0.1)
      if GPIO.input(GPIO_switch)==False and run == True:
         print ("  Stopped ") 
         run = False
         os.killpg(p.pid, signal.SIGTERM)
         while GPIO.input(GPIO_switch)==False:
             time.sleep(0.1)
       

except KeyboardInterrupt:
  print ("  Quit")
  GPIO.cleanup() 
