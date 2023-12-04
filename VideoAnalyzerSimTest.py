from VideoAnalyzerSim import VideoAnalyzer
from MouseMonitor import MouseMonitor
import time


# main code for VideoAnalyzerSim unit test
print("test program for VideoAnalyzerStub")
videoAnalyzer = VideoAnalyzer()
mouse1 = MouseMonitor(1)
mouse2 = MouseMonitor(2)

for i in range(10):
    locations = videoAnalyzer.process_single_frame()
    print(locations)
    print(mouse1.get_mouse_location(locations))
    print(mouse2.get_mouse_location(locations))
    time.sleep(5)

print ("program terminated")