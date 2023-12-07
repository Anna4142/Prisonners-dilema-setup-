from ValveControl import ValveControl
import threading
import time

class RewardManager:
    def __init__(self, arduino_instance, valve_channels):
        self.valve_channels = valve_channels
        self.valves = [ValveControl(channel, arduino_instance) for channel in valve_channels]

    def _valve_number_to_index(self, valve_number):
        if valve_number in self.valve_channels:
            return self.valve_channels.index(valve_number)
        else:
            return None

    def _threaded_deliver(self, valve_index, duration):

        if valve_index is not None and valve_index < len(self.valves):
            valve = self.valves[valve_index]
            valve.OpenValve(duration)
            while valve.IsValveOpen():
               time.sleep(0.0001)
        # Wait a bit before checking again to avoid overloading the CPU
        else:
            print(f"Valve index {valve_index} is out of range.")

    def _get_valve_index(self, scenario, mouse_id):
        mapping = {
            'cc': {1: 12, 2: 7},
            'cd': {1: 12, 2: 9},
            'dc': {1: 10, 2: 7},
            'dd': {1: 10, 2: 11},
            'center': {1: 11, 2: 8},
        }
        valve_number = mapping.get(scenario, {}).get(mouse_id)
        return self._valve_number_to_index(valve_number)

    def deliver_reward(self, scenario, mouse_id, reward_time):
        valve_index = self._get_valve_index(scenario, mouse_id)
        if valve_index is not None:
            thread = threading.Thread(target=self._threaded_deliver, args=(valve_index, reward_time))
            thread.start()
            thread.join()

# Example usage:
# arduino_instance = Arduino()  # This should be your actual Arduino instance
# valve_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Example channel numbers for your valves
# reward_manager = RewardManager(arduino_instance, valve_channels)

# To deliver a reward, call:
# reward_manager.deliver_reward('cc', 1, 5)  # 'cc' scenario, mouse_id 1, for 5 seconds



