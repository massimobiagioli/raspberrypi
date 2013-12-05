'''
Serial Mock
'''
class SerialMock:
    
    def __init__(self, port):
        self.__port = port
        self.__status = [0 for x in range(4)]
    
    def write(self, buffer):
        encoded = buffer.encode('hex')
        channel = int(encoded[3])
        command = int(encoded[5])
        
        if (9 == channel):
            tmp = chr(self.__status[0] + self.__status[1] + self.__status[2] + self.__status[3])
            return tmp
        else:
            self.__status[channel - 1] = command
        
    def close(self):
        pass

