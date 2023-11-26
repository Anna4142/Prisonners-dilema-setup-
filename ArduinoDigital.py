import serial

class ArduinoDigital:
    def __init__(self, portname):
        self.comport = serial.Serial(portname, 9600)

    def DigitalHigh(self, pin):
        outbyte = pin.to_bytes(1, 'big')
        self.comport.write(outbyte)
        outbyte = (1).to_bytes(1, 'big')
        self.comport.write(outbyte)

    def DigitalLow(self, pin):
        outbyte = pin.to_bytes(1, 'big')
        self.comport.write(outbyte)
        outbyte = (0).to_bytes(1, 'big')
        self.comport.write(outbyte)
