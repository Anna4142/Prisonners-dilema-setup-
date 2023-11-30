import tkinter as tk
from ExperimentManager import ExperimentManager
from experimentgui import *
import tkinter as tk




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
            opponent_strategy = settings.get('opponent_strategy')
            opponent_type = settings.get('opponent_type')  # Make sure 'opponent_type' is included in the settings

            # Modify num_trials as per your requirement
            num_trials += 2

            # Initialize and start the experiment
            expManager = ExperimentManager()
            print("Experiment manager now running")
            expManager.start_streaming_exp(num_trials, trial_duration, decision_time, opponent_type, opponent_strategy)
            del expManager
        else:
            print("No valid settings were provided.")



if __name__ == "__main__":
    main()


