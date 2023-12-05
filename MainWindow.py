from ExperimentManager import ExperimentManager
from experimentgui import *

def main():
        # Create an instance of the ExperimentGUI class
        experiment_gui = ExperimentGUI()
        experiment_gui.setup_gui()

        # After the GUI is closed, get the settings using the get_settings method
        settings = experiment_gui.on_start_clicked()

        if settings:
            # Extract the necessary parameters from the settings
            num_trials = settings.get('num_trials')
            trial_duration = settings.get('trial_duration')
            decision_time = settings.get('decision_time')

            opponent_type = settings.get('opponent_type')  # Make sure 'opponent_type' is included in the settings
            if opponent_type=="mouse_computer":
                opponent_strategy_1 = settings.get('opponent_strategy')
                opponent_strategy_2= settings.get('computer_opponent_strategy')
            elif  opponent_type =="computer_computer":
                opponent_strategy_1 = settings.get('opponent_strategy')
                opponent_strategy_2 = settings.get('computer_opponent_strategy')
            else:

                opponent_strategy_1 = settings.get('opponent_strategy')
                opponent_strategy_2 = settings.get('computer_opponent_strategy')
            # Modify num_trials as per your requirement
            num_trials += 2

            # Initialize and start the experiment
            expManager = ExperimentManager()
            print("Experiment manager now running")
            expManager.start_streaming_exp(num_trials, trial_duration, decision_time, opponent_type, opponent_strategy_1,opponent_strategy_2)
            del expManager
        else:
            print("No valid settings were provided.")



if __name__ == "__main__":
    main()


