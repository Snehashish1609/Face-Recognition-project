import pyfirmata
import time
import serial
import pymongo

#Database
client = pymongo.MongoClient('localhost', 27017)
db = client.project

pl = ['D9F8BA98', 'B39E3A33']

'''board = pyfirmata.Arduino('COM5')
print("Arduino communication started!")
while True:
    board.digital[13].write(1)
    time.sleep(0.5)
    board.digital[13].write(0)
    time.sleep(0.5)'''

'''device = 'COM5' # this will have to be changed to the serial port being used!
try:
  print("Trying...",device) 
  arduino = serial.Serial(device, 9600) 
except: 
  print("Failed to connect on",device)
while True:
    time.sleep(1)
    data = arduino.readline()
    t = data.decode('UTF-8')
    t = t.replace('\r', '')
    t = t.replace('\n', '')
    t = t.replace(' ', '')

    # Product info
    print(t)
    res = db.product.find_one( {"product_id" : t}, {"_id" : 0} )
    print(res)
    print("-------------------------------")'''

def basketScanner():
  product_list = []
  device = 'COM5'
  try:
    arduino = serial.Serial(device, 9600)
  except:
    print("Failed to connect on", device)
  
  # Running the scanner for 10 secs
  t_end = time.time() + 10
  while time.time() < t_end:
    data = arduino.readline()
    t = data.decode('UTF-8')
    t = t.replace('\r', '')
    t = t.replace('\n', '')
    t = t.replace(' ', '')

    # Product info
    print(t)
    product_list.append(t)
    
    # res = db.product.find_one( {"product_id" : t}, {"_id" : 0} )
  return product_list

def productInfo(product_list):
  prod_info_list = []
  for i in product_list:
    res  = db.product.find_one( {"product_id" : i }, {"_id" : 0} )
    prod_info_list.append(res)
  return prod_info_list

def findTotal(product_list):
  total = 0
  for i in product_list:
    res = db.product.find_one( {"product_id" : i}, { "_id" : 0, "name" : 0, "product_id" : 0} )
    total = total + float(res["price"])
  return total

print(productInfo(pl))
print(findTotal(pl))