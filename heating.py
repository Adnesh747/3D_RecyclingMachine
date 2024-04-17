import serial
import time
import threading
import RPi.GPIO as gpio

element_pin = 17
extruder_pin = 27
h1 = 1 
h2 = 1
def setup():

	gpio.setmode(gpio.BCM)
	gpio.setup(element_pin,gpio.OUT) #Element
	gpio.setup(extruder_pin,gpio.OUT) #Extruder

def write_SSElement(id):
    try:
        with open("/home/pi/SSElement","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write Extrude;llrTemp:",e)

def write_status(id):
    try:
        with open("/home/pi/status","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write status:",e)
def write_SSExtruder(id):
    try:
        with open("/home/pi/SSExtruder","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write ExtruderTemp:",e)


def read_ActualElementTemp():
   try:
        f = open("/home/pi/ActualElementTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_ActualExtruderTemp():
   try:
        f = open("/home/pi/ActualExtruderTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_HeatingTemp():
   try:
        f = open("/home/pi/HeatingTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_ExtruderTemp():
   try:
        f = open("/home/pi/ExtruderTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id


def HeatControls():
 
 global h1, h2 

 try:
   AElement = float(read_ActualElementTemp().strip())
   setElement = float(read_HeatingTemp().strip())
 except ValueError:
   setElement = 0
 try:
   AExtruder = float(read_ActualExtruderTemp().strip())
   setExtruder = float(read_ExtruderTemp().strip())
 except ValueError:
   setExtruder = 0

 target1 = setElement * 0.02
 target15 = setElement * 0.05
 target2 = setExtruder * 0.02
 target25 = setExtruder * 0.05

 if setElement<= 210 and AElement<setElement and abs(AElement - setElement)>target1:
   #heat it up
   gpio.output(element_pin,gpio.HIGH)
   write_SSElement("no")
   print("heating element")
   write_status("2")
# elif setElement>=180 and AElement>setElement and abs(AElement - setElement)>target1:

 elif abs(AElement-setElement)<=target15:
   write_status("1")
   write_SSElement("yes")
   if h1 == 1:
     gpio.output(element_pin,gpio.HIGH)
     h1 = 0
   if h1 == 0:
     gpio.output(element_pin,gpio.LOW) 
     h1 = 1
   print("steady state")
 else: 
   write_SSElement("no")
   gpio.output(element_pin,gpio.LOW)
   print("Cooling down element")
 #Cool it down
 if setExtruder<=275 and AExtruder<setExtruder and abs(AExtruder - setExtruder)> target2:
#heat
   print("heating extruder  up")
   gpio.output(extruder_pin,gpio.HIGH)
   write_SSExtruder("no")
   write_status("2")
 elif abs(AExtruder - setExtruder) <= target2:
   write_SSExtruder("yes")
   write_status("1")
   if h2 == 1:
     gpio.output(element_pin,gpio.HIGH)
     h2 = 0
   if h2 == 0: 
     gpio.output(element_pin,gpio.LOW)
     h2 = 1 
   print("steady state")
 else:
   write_SSExtruder("no")
   gpio.output(extruder_pin,gpio.LOW)
   print("Cooling down extruder")
   print(str(setExtruder) + str(AExtruder) + str(target2))
#cool


if __name__ == '__main__':
 
 setup()
 h1 =1
 h2 = 1
 try:
   while True:
       HeatControls()
       time.sleep(3)
 except KeyboardInterrupt:
   gpio.cleanup()
   print("Exiting")
