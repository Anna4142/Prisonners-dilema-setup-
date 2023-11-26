import datetime


class ArduinoDigital:
    def __init__(self, portname):
        self.comport = portname

    def DigitalHigh(self, pin):
        ct = datetime.datetime.now().strftime("%M:%S.%f")
        print("Arduino Digital channel ", pin, "set to High. Time Stamp= ", ct)

    def DigitalLow(self, pin):
        ct = datetime.datetime.now().strftime("%M:%S.%f")
        print("Arduino Digital channel ", pin, "set to Low. Time Stamp= ", ct)