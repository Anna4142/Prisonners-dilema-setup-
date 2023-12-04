from enum import Enum
from locations import Locations

class MouseMonitor:
    def __init__(self, mouse_id):
        self.mouse_id = mouse_id

    def get_mouse_location(self, zones_list, other_mouse_location):
        # Split the zones based on mouse_id
        mouse_zones = zones_list[(self.mouse_id - 1) * 3 : self.mouse_id * 3]

        # Interpret the zones list to return the corresponding location
        location = Locations.Unknown
        if mouse_zones[0] == 1:
            location = Locations.Cooperate
        elif mouse_zones[1] == 1:
            location = Locations.Center
        elif mouse_zones[2] == 1:
            location = Locations.Defect

        return location



