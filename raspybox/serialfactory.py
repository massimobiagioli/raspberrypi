'''
Serial Factory
'''
from common import DEBUG
from serialmock import SerialMock
import serial


class SerialFactory:
    
    def getSerial(self, port):
        if (0 == DEBUG):
            return serial.Serial(port)
        else:
            return SerialMock(port)