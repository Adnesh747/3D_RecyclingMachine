import csv
import time
#import pandas as pd

import numpy as np
import statsmodels.api as sm

def count_csv_rows(filename):
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            row_count = sum(1 for row in csv_reader)
            return row_count
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return "error"

def read_csv_columns(filename):
    columns = {}  # Dictionary to store columns

    # Open CSV file for reading
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Read the first row to get column headers
        headers = next(csv_reader)
        
        # Initialize empty lists for each column
        for header in headers:
            columns[header] = []
        
        # Read remaining rows and store data in respective columns
        for row in csv_reader:
            for i, value in enumerate(row):
                columns[headers[i]].append(value)
    
    return columns
def read_auger_speed():
   try:
        f = open("/home/pi/AugerSpeed","r")
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



def write_to_csv(filename, new_data):
    # Open CSV file for reading and writing
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  # Read existing headers
        
        # Read existing data
        columns = {}
        for header in headers:
            columns[header] = []
        for row in csv_reader:
            for i, value in enumerate(row):
                columns[headers[i]].append(value)
    
    # Append new data to columns
    for header, value in new_data.iteritems():
        columns[header].append(value)
    
    # Write data to the CSV file
    with open(filename, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the headers
        csv_writer.writerow(headers)
        
        # Write data row by row
        rows = zip(*[columns[header] for header in headers])
        for row in rows:
            csv_writer.writerow(row)


def datahandle():
# Example usage:
   filename = "my_data.csv"
   read_heating = float(read_ActualElementTemp())
   read_extruder = float(read_ActualExtruderTemp())
   time.sleep(5)
   read_heating2 = float(read_ActualElementTemp())
   read_extruder2 = float(read_ActualExtruderTemp())
   read_auger = read_auger_speed()

   if abs(read_heating - read_heating2) / read_heating <= 0.05 and \
       abs(read_extruder - read_extruder2) / read_extruder <= 0.05 and \
       count_csv_rows(filename) <=100:
# Example data to append to the CSV file
     new_data = {
      "Auger Speed": read_auger,
      "Heating Temperature": str(read_heating2),
      "Extruder Temperature": str(read_extruder2),
      "Exit Quality": 200
     }
     write_to_csv(filename, new_data)

# Read and print the updated CSV file
   print("Updated CSV file:")
   columns = read_csv_columns(filename)
   for header, values in columns.iteritems():
      print(header + ":", values)

if __name__ == '__main__':

 try:
  while True:
 #  datahandle()
    pass
 except KeyboardInterrupt:
  print("Stopping")
