from enum import Enum
from locations import Locations

class MouseMonitor:
    def __init__(self, videoAnalyzer, mouse_id):
        self.videoAnalyzer = videoAnalyzer
        self.mouse_id = mouse_id

    def get_mouse_location(self):
        zones = self.videoAnalyzer.get_mouse_location()
        # Split the zones based on mouse_id
        mouse_zones = zones[(self.mouse_id - 1) * 3:self.mouse_id * 3]
        return self.decode_zones(mouse_zones)

    def decode_zones(self, zones_list):
        # Interpret the zones list to return the corresponding location
        if zones_list[0] == 1:
            return Locations.Cooperate  # 'Up' arrow was pressed
        elif zones_list[1] == 1:
            return Locations.Center     # 'Left' arrow was pressed
        elif zones_list[2] == 1:
            return Locations.Defect     # 'Down' arrow was pressed

        return Locations.Unknown  # If no pattern is matched, return Unknown



