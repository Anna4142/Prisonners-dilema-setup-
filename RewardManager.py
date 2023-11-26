from ValveControl import ValveControl
import threading

class RewardManager:
    def __init__(self, arduino_instance, valve_channels):
        # Initialize ValveControl objects for each channel
        self.valves = [ValveControl(channel, arduino_instance) for channel in valve_channels]

    def _threaded_deliver(self, valve_index, duration):
        # Open the valve at the specified index for the given duration
        self.valves[valve_index].OpenValve(duration)

    def _get_valve_index(self, scenario, mouse_id):
        # Define a mapping based on the scenario and mouse_id
        mapping = {
            'cc': {1: 12, 2: 7},
            'cd': {1: 12, 2: 9},
            'dc': {1: 10, 2: 7},
            'dd': {1: 10, 2: 11},
            'center': {1: 11, 2: 8},
        }

        # Retrieve the mapping for the given scenario and mouse_id
        return mapping.get(scenario, {}).get(mouse_id, None)

    # The methods to deliver rewards based on scenarios
    # You may need to add the logic to determine the scenario and call the appropriate method

    def deliver_reward(self, scenario, mouse_id, reward_time):
        valve_index = self._get_valve_index(scenario, mouse_id)
        if valve_index is not None:
            print('REWARD DELIVERED AT VALVE',valve_index)
            # Start the delivery in a new thread
            thread = threading.Thread(target=self._threaded_deliver, args=(valve_index, reward_time))
            thread.start()
            thread.join()  # Wait for the thread to finish if necessary

# Example usage:
# arduino_instance = Arduino()  # This should be your actual Arduino instance
# valve_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Example channel numbers for your valves
# reward_manager = RewardManager(arduino_instance, valve_channels)

# To deliver a reward, call:
# reward_manager.deliver_reward('cc', 1, 5)  # 'cc' scenario, mouse_id 1, for 5 seconds

