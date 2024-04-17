import time
def write_ExtruderTemp(id):
    try:
        with open("/home/pi/ExtruderTemp","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write ExtruderTemp:",e)
def write_HeatingPower(id):
    try:
        with open("/home/pi/HeatingPower","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write HeatingPower:",e)
def read_Automode():
   try:
        f = open("/home/pi/automode","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_Gon():
   try:
        f = open("/home/pi/var/Gon","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_SSElement():
   try:
        f = open("/home/pi/SSElement","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_SSExtruder():
   try:
        f = open("/home/pi/SSExtruder","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

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

def read_Exittemp():
   try:
        f = open("/home/pi/Exittemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def write_grinderon(id):
    try:
        with open("/home/pi/grinderon","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write grinder on:",e)
def write_AugerSpeed(id):
    try:
        with open("/home/pi/AugerSpeed","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write AugerSpeed:",e)
def Automode():
 Autoison = read_Automode().strip()
 if Autoison == "on":
       Gon = read_Gon().strip()
       if Gon == "1":
        print("turned G on")
        write_grinderon("yes")
        time.sleep(1)
        write_grinderon("off") 
       else:
         write_grinderon("off")
       
       #AElement = read_ActualElementTemp().strip()
       #AExtruder = read_ActualExtruderTemp().strip() 
       SS1 = read_SSElement().strip()
       SS2 = read_SSExtruder().strip()
       if SS1 == "yes" and SS2 == "yes":
          Target_temp = 190
          try:
            setElement = float(read_HeatingTemp().strip())
            setExtruder = float(read_ExtruderTemp().strip())
            Current_temp = float(read_Exittemp().strip())
          except ValueError:
            print("error converting values")
          Range_target = Target_temp*0.02
          if abs(Current_temp - Target_temp) <= Range_target:
              pass
          else:
            changed = 0
            if Current_temp<Target_temp and setExtruder<280:
               changed = 1
               new_setpoint = setExtruder + 5
               new_setpoint2 = setElement
            elif Current_temp<Target_temp and setExtruder>=275 and setElement < 200:
               changed = 1
               new_setpoint2 = setElement + 5
               new_setpoint = setExtruder
            elif Current_temp>Target_temp and setExtruder>180:
               changed = 1
               new_setpoint = setExtruder - 5
               new_setpoint2 = setElement
            if changed == 1:
             write_ExtruderTemp(str(new_setpoint))
             write_HeatingPower(str(new_setpoint2))
            else:
              print("nothing changed")



 else:
   pass

if __name__ == '__main__':
 try:
  while True:
    time.sleep(5)
    Automode()
 except KeyboardInterrupt:
  print("exiting Auto Program")
