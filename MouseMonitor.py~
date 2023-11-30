from enum import Enum
from locations import Locations##new locations class-Anushka
class MouseMonitor:
    def __init__(self, data_queue, mouse_id):
        self.data_queue = data_queue
        self.mouse_id = mouse_id

    def get_mouse_location(self):

            zones = self.data_queue.get()
            #print("zones", zones)
            return self.decode_zones(zones)


    def decode_zones(self, zones_list):
        if zones_list[0] == 1:
            return Locations.Cooperate  # 'Left' arrow was pressed
        elif zones_list[1] == 1:
            return Locations.Center     # 'Down' arrow was pressed
        elif zones_list[2] == 1:
            return Locations.Defect     # 'Right' arrow was pressed
        return Locations.Unknown  # If no pattern is matched, return Unknown



#ANUSHKA-CHANGE IN LOCATION KEY DECODING
#Left arrow for Cooperate ([1, 0, 0]),
#Down arrow for Center ([0, 1, 0]),
#Right arrow for Defect ([0, 0, 1]),
#Up arrow for Default ([0, 0, 0]).


