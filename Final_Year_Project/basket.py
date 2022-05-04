import pyfirmata
import time

board = pyfirmata.Arduino('COM5')
print("Arduino communication started!")
while True:
    board.digital[13].write(1)
    time.sleep(0.5)
    board.digital[13].write(0)
    time.sleep(0.5)