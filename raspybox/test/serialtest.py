from common import RELAY_BOARD_COM_PORT
import serial

ser = serial.Serial(RELAY_BOARD_COM_PORT)
ser.write(chr(255) + chr(1) + chr(0))
ser.close()

