import serial
import time

def write_t(id):
    try:
        f = open("/home/pi/t","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return
def write_t2(id):
    try:
        f = open("/home/pi/t2","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return
def write_error(id):
    try:
        f = open("/home/pi/errormess","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return

def read_grinder_speed():
   try:
        f = open("/home/pi/grinderspeed","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_grinderon():
    try:
        f = open("/home/pi/grinderon","r")
        id = f.read()
        f.close()
    except:
        id = "0"
    return id

def read_lock():
    try:
        f = open("/home/pi/lock","r")
        id = f.read()
        f.close()
    except:
        id = "0"
    return id
def read_auger():
    try:
        f = open("/home/pi/AugerSpeed","r")
        id = f.read()
        f.close()
    except:
        id = "0"
    return id



if __name__=='__main__':
    ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1.0)
    time.sleep(3)
    ser.reset_input_buffer()
    print("Serial OK")
#    send_data_to_aurdino
    try:
        while True:
            # time.sleep(1)  # Uncomment this line if you need a delay
            readGs1 = read_grinderon().strip()
            readGs = read_grinder_speed().strip("\n")
            readAuger = read_auger().strip()
            locksend = read_lock().strip()
            info = readGs1 + "\n" + readGs + "\n" + locksend
            print(info)
            ser.write(info.encode('utf-8'))
            while ser.in_waiting <=0:
                time.sleep(0.01)
            response = ser.readline().decode('utf-8').rstrip()
            print("Retrieved" + response)
            write_error(response)
            errormess = response
            if readGs == "1":
                t = 0.001
            elif readGs == "2":  # Use elif for subsequent conditions
                t = 0.0001
            elif readGs == "0":
                t = 1
   #         elif readGs == "3":  # Corrected the case of readGs
    #            t = 0.0001
            if readAuger == "1":
                t2 = 0.001
            elif readAuger == "2":
                t2 = 0.0001
            elif readAuger == "0":
                t2 = 1
            write_t(t)
            write_t2(t2)
            #GrinderPower = readGs1
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected in send_data_to_aurdino")
#        gpio.cleanup()
        ser.close()
