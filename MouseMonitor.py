from enum import Enum
from locations import Locations##new locations class-Anushka


class MouseMonitor:
    def __init__(self, video_analyzer_instance, mouse_id):
        self.video_analyzer = video_analyzer_instance
        self.mouse_id = mouse_id

    def get_mouse_location(self,zones):

        # Split the zones based on mouse_id
        zones_list = zones[(self.mouse_id - 1) * 3:self.mouse_id * 3]



        if zones_list[0] == 1:
            location= Locations.Cooperate  # 'Up' arrow was pressed
        elif zones_list[1] == 1:
            location=Locations.Center     # 'Left' arrow was pressed
        elif zones_list[2] == 1:
            location = Locations.Defect     # 'Down' arrow was pressed
        else:
            location = Locations.Unknown  # If no pattern is matched, return Unknown


        return location
