from enum import Enum

class Locations(Enum):
    Unknown = 0
    Cooperate = 1
    Center = 2
    Defect = 3

class mouseMonitor:
    def __init__(self, videoAnalyzer):
        self.videoAnalyzer = videoAnalyzer

    def GetMouseLocation(self, mouse_loc):  # added parameters
        zones = self.videoAnalyzer.process_frame()  # renamed method and added parameters

        # Assuming zones list is structured as: [cooperate_mouse1, center_mouse1, defect_mouse1, cooperate_mouse2, center_mouse2, defect_mouse2]
        mouse1_zones = zones[:3]
        mouse2_zones = zones[3:]



        return mouse2_zones,mouse1_zones
