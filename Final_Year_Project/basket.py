import pyfirmata
import time
import serial

'''board = pyfirmata.Arduino('COM5')
print("Arduino communication started!")
while True:
    board.digital[13].write(1)
    time.sleep(0.5)
    board.digital[13].write(0)
    time.sleep(0.5)'''

device = 'COM5' # this will have to be changed to the serial port being used!
try:
  print("Trying...",device) 
  arduino = serial.Serial(device, 9600) 
except: 
  print("Failed to connect on",device)
while True:
    time.sleep(1)
    data = arduino.readline()
    print(data)
    #pieces = data.split(" ")
    #print(*pieces, sep = " ")
    print("-------------------------------")