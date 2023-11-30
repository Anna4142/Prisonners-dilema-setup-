from enum import Enum
from locations import Locations##new locations class-Anushka


class MouseMonitor:
    def __init__(self, video_analyzer_instance, mouse_id):
        self.video_analyzer = video_analyzer_instance
        self.mouse_id = mouse_id

    def get_mouse_location(self,zones):
        #print(type(self.video_analyzer))
        #self.video_analyzer.stream_and_process()  ###for the actual video analyser
        #zones = self.video_analyzer.get_zone_activations()

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






