from gpiozero import Button
import sys
import os
import subprocess
from signal import pause

button = Button(17)
p = subprocess.Popen(['python', 'objectident.py', 'arg1', 'arg2'])
##press = button.when_pressed
restart = True


##def turn_camera_on():
	##print("camera is on")
	##os.system("python objectident.py")
	
##def turn_camera_off():
	##print("camera is not on")
	##p.terminate()		
	##p.wait()


##for x in press: 
	##if x == True:
		##turn_camera_off
	##elif x == False:
		##turn_camera_on

while restart:

	while button.is_pressed == True:

		if button.is_pressed:
			print("camera is not on")
			os.system("kill -9 %d"%(os.getppid())
			
		else
			print("camera is on")
			os.system("python objectident.py")
			
			
			
		
		
		



