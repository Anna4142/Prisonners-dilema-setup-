from pynput.keyboard import Key, Listener
import time

class VideoAnalyzer:
    def __init__(self):
        self.mouseLocations = [0] * 6  # a list of 6 zeros
        self.mouse = 1
        listener = Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()  # start to listen on a separate thread

    def on_press(self, key):
        if key == Key.shift:
            self.mouse = 2
        if key == Key.left:
            self.updateLocations([1, 0, 0], self.mouse)
        elif key == Key.right:
            self.updateLocations([0, 0, 1], self.mouse)
        elif key == Key.down:
            self.updateLocations([0, 1, 0], self.mouse)
        elif key == Key.up:
            self.updateLocations([0, 0, 0], self.mouse)

    def on_release(self, key):
        if key == Key.shift:
            self.mouse = 1

    def updateLocations(self, locations, mouse):
        if mouse == 1:
            self.mouseLocations = locations + self.mouseLocations[3:]
        else:
            self.mouseLocations = self.mouseLocations[:3] + locations

    def process_single_frame(self):
        return self.mouseLocations

# Assuming MouseMonitor is defined elsewhere in your code
from MouseMonitor import MouseMonitor

# main code for VideoAnalyzerSim unit test
print("test program for VideoAnalyzerStub")
videoAnalyzer = VideoAnalyzer()
# Assuming MouseMonitor is initialized as follows
mouse1 = MouseMonitor(videoAnalyzer,1)
mouse2 = MouseMonitor(videoAnalyzer,2)

for i in range(10):
    locations = videoAnalyzer.process_single_frame()
    print(locations)
    # Assuming get_mouse_location is a method of MouseMonitor
    print(mouse1.get_mouse_location(locations))
    print(mouse2.get_mouse_location(locations))
    time.sleep(5)

print("program terminated")
