import sys
import pprint
sys.path.insert(0,".")

#pprint.pprint(sys.path)
sys.path.insert(6,'/home/pi/.local/lib/python2.7/site-packages')
#pprint.pprint(sys.path)
#sys.path.insert(0,'/home/pi')
#pprint.pprint(sys.path)

import time
import os
import gspread
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = '/home/pi/app/key.json'
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
def read_error():
   try:
        f = open("/home/pi/errormess","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_grinder_speed():
   try:
        f = open("/home/pi/grinderspeed","r")
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

def write_grinder_speed(id):
    try:
        f = open("/home/pi/grinderspeed","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return

def write_lock(id):
    try:
        f = open("/home/pi/lock","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return
def read_grinderon():
    try:
        f = open("/home/pi/grinderon","r")
        id = f.read()
        f.close()
    except:
        id = "0"
    return id
def write_grinderon(id):
    try:
        f = open("/home/pi/grinderon","w")
        f.write(str(id))
        f.close()
    except:
        id = "0"
    return

def pulll():
#	print("entered the function")
#	time.sleep(2)
	creds = None
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)

#	print("It got to here")
	SAMPLE_SPREADSHEET_ID = '18k0f4JPtuxMIjAun9RV689vLWqHiXG5r1MbUwbMrS2I'
#	print("its in here")
#	service = build('sheets','v4',credentials=creds)
#	try:
#		service = build('sheets', 'v4', credentials=creds)
#	except Exception as e:

#		print("An error occurred while creating the service:", e)
	client = gspread.authorize(creds)
	try:
#		print("top")
		sheet = client.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1
#		print(sheet)
	except Exception as e:
		print("There is an error")

#	print("new spot")

	grinder_speed = sheet.acell('E2').value
	grinder_power = sheet.acell('G2').value

	print("Grinder Speed:", str(grinder_speed))
#	print("The machine power status is:",str(grinder_power))
	locks = sheet.acell('K2').value
	write_lock(locks)
#	sheet = service.spreadsheets()
#	Match= sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="res!F2:F2").execute()
#	GrinderSpeed = Match.get('values',[])

#	print("Club ID : " + GrinderSpeed[0][0])
#	print("Lock Status",str(locks))

	write_grinderon(grinder_power)
	write_grinder_speed(grinder_speed)

	readerror = read_error()
	sheet.update('J2',str(readerror)) 
	readGs1 = read_grinderon()
	sheet.update('A9',str(readGs1))
	readGS = read_grinder_speed()
	sheet.update('A4', str(readGS))
	readLock = read_lock()
	sheet.update('A10',str(readLock))


def main():
    try:
        while True:
            pulll()
            # load_ip()  # If you have another function to call
            time.sleep(1)
    except Exception as e:
        print("Exception occurred:", e)
        print("Reloading in 3 seconds...")
        time.sleep(3)


if __name__ == "__main__":
	main()
