import csv

class TrialLogger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.csv_file = open(self.file_path, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Trial Number", "Trial validity", "Opponent Choice", "Mouse choice", "Reward","opponent reward"])

    def log_trial_data(self, trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,opponent_reward):
        self.csv_writer.writerow([trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,opponent_reward])

    def finalize_logging(self):
        self.csv_file.close()
