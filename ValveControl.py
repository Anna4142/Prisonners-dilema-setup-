import time


class ValveControl:
    def __init__(self, channel, arduino):
        self.channel = channel
        self.arduino = arduino
        self.arduino.DigitalLow(self.channel)
        self.starttime = 0
        self.duration = 0
        self.valveopen = False

    def OpenValve(self, duration):
        self.starttime = time.time()
        self.duration = duration
        self.arduino.DigitalHigh(self.channel)
        self.valveopen = True

    def IsValveOpen(self):
        if self.valveopen:
            if time.time() - self.starttime > self.duration:
                self.arduino.DigitalLow(self.channel)
                self.starttime = 0
                self.duration = 0
                self.valveopen = False
        return self.valveopen


