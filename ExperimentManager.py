import time
import threading
from VideoAnalyzer import VideoAnalyzer
from MouseMonitor import MouseMonitor
from VideoAnalyzerStub import VideoAnalyzerStub
from MouseMonitor import Locations
from logger import TrialLogger
from simulated_mouse import Simulated_mouse
#from ArduinoDigital import ArduinoDigital
from ArduinoDigitalSim import ArduinoDigital
from StateManager import StateManager
from StateManager import States
from StateManager import Events
import experimentgui
from RewardManager import RewardManager
import tkinter as tk
from logger import TrialLogger
from ArduinoDigitalSim import ArduinoDigital  ##Anushka-new class

from queue import Queue
class ExperimentManager:
    def __init__(self):
        # Initialize other components here
        #self.videoAnalyser = VideoAnalyzer()

        self.mouse_location_queue = Queue()



        #self.videoAnalyser = VideoAnalyzerStub(self.root, self.mouse_location_queue)##puts data into queue
        self.trial_logger = TrialLogger("C:/Users/anush/Downloads/PrisonerDilemmaPy_(4)")
        #self.mouse1 = MouseMonitor(self.mouse_location_queue, mouse_id=1)#gets data from queue
        #self.mouse2 = MouseMonitor(self.mouse_location_queue, mouse_id=2)
        self.root = tk.Tk()
        self.root.withdraw()
        self.mouse_location_queue_1 = Queue()
        self.mouse_location_queue_2 = Queue()

        # Main window for the first mouse
        self.top_level_1 = tk.Toplevel(self.root)
        self.video_analyzer_1 = VideoAnalyzerStub(self.top_level_1, self.mouse_location_queue_1)
        self.mouse1 = MouseMonitor(self.mouse_location_queue_1, mouse_id=1)

        # Separate window for the second mouse
        self.top_level_2 = tk.Toplevel(self.root)
        self.video_analyzer_2 = VideoAnalyzerStub(self.top_level_2, self.mouse_location_queue_2)
        self.mouse2 = MouseMonitor(self.mouse_location_queue_2, mouse_id=2)
        #self.mouse1 = MouseMonitor(self.videoAnalyser, 1)
        #self.mouse2 = MouseMonitor(self.videoAnalyser, 2)
        self.opponent1 = Simulated_mouse(self.mouse_location_queue_2,mouse_id=1)
        self.opponent2 = Simulated_mouse(self.mouse_location_queue_1,mouse_id=2)
        self.numcompletedtrial=0
        self.stateManager = StateManager()

        # Initialize Arduino board
        self.initialize_arduino()

        # Set default reward and punishment times
        self.reward_time = 0.02
        self.sucker_time = 0
        self.temptation_time = 0.009
        self.punishment_time = 0.004
        self.center_reward_time = 0.1

        # Initialize CSV file and video capture
        #self.initialize_csv_logging()
        #self.initialize_video_capture()


        ### VARIABLES FOR LOG FILE INITIALLY INITIALIZED TO FALSE
        self.data_file_loc = 'path_to_csv_file.csv'
        self.cc_var = False
        self.cd_var = False
        self.dc_var = False
        self.dd_var = False
        self.center_var = False
        self.no_trial_var = False

        self.cc_cnt = 0
        self.cd_cnt = 0
        self.dc_cnt = 0
        self.dd_cnt = 0
        self.center_cnt = 0

        self.reward_manager = RewardManager(self.board, [7, 8, 9, 10, 11, 12])
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    def initialize_arduino(self):
        comport="5"
        self.board = ArduinoDigital(comport)
        # Set all pins to low
        for pin in [7, 8, 9, 10, 11, 12]:
            self.board.DigitalLow(pin)
    def start_gui(self):
        self.root.mainloop()
    def start_gui_in_thread(self):
        # Start GUI in a new thread
        gui_thread = threading.Thread(target=self.start_gui)
        gui_thread.start()

    def on_close(self):
        # Destroy the Toplevel windows
        self.top_level_1.destroy()
        self.top_level_2.destroy()

        # Finally, destroy the main window
        self.root.destroy()
    def start_experiment_in_thread(self, num_trial, duration, time_decision, opponent_type, opponent_strategy):
        # Start streaming experiment in a new thread
        experiment_thread = threading.Thread(target=self.start_streaming_exp, args=(num_trial, duration, time_decision, opponent_type, opponent_strategy))
        experiment_thread.start()
    def StateActivity(self, state):
        trialcompleted = False

        if state == States.Start:
            # Initialize variables, set some flags, start recording, etc.
            pass


        elif state == States.TrialControl:
            # Increment the trial number counter in the TrialControl state
            self.numcompletedtrial += 1
            # Determine the next state based on the total number of trials
            if self.numcompletedtrial >= self.total_number_of_trials:
                self.current_state = States.End
            else:
                self.current_state = States.TrialStarted

            trial_number = self.numcompletedtrial   # Adjust as needed
            trial_validity = (
                    (self.cc_var and self.center_var) or
                    (self.cd_var and self.center_var) or
                    (self.dc_var and self.center_var) or
                    (self.dd_var and self.center_var)
            )
            if self.cc_var:
                mouse_choice = "C"
                opponent_choice = "C"
                mouse_reward="12ml"
                opponent_reward="12ml"
            elif self.cd_var:
                mouse_choice = "C"
                opponent_choice = "D"
                mouse_reward ="0ml"
                opponent_reward ="15ml"
            elif self.dc_var:
                mouse_choice = "D"
                opponent_choice = "C"
                mouse_reward ="15ml"
                opponent_reward ="0ml"
            elif self.dd_var:
                mouse_choice = "D"
                opponent_choice = "D"
                mouse_reward ="15ml"
                opponent_reward ="15ml"
            else:
                # Handle the case when none of the conditions are met
                mouse_choice = "N/A"
                opponent_choice = "N/A"
                mouse_reward ="-"
                opponent_reward ="-"
            self.trial_logger.log_trial_data(trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,
                                             opponent_reward)

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.cc_var = True
            self.cc_cnt += 1
            self.reward_manager.deliver_reward('cc', 12, self.reward_time)
            self.reward_manager.deliver_reward('cc', 7, self.reward_time)

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.cd_var = True
            self.cd_cnt += 1
            self.reward_manager.deliver_reward('cd', 12, self.reward_time)
            self.reward_manager.deliver_reward('cd', 9, self.punishment_time)

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.dc_var = True
            self.dc_cnt += 1
            self.reward_manager.deliver_reward('dc', 10, self.punishment_time)
            self.reward_manager.deliver_reward('dc', 7, self.reward_time)

        elif state == States.M1DM2D:
            # Actions for M1DDM2D state
            self.dd_var = True
            self.dd_cnt += 1
            self.reward_manager.deliver_reward('dd', 10, self.punishment_time)
            self.reward_manager.deliver_reward('dd', 9, self.punishment_time)

        elif state == States.WaitForReturn:
            # Handle WaitForReturn state
            pass  # Placeholder for WaitForReturn logic

        elif state == States.TrialCompleted:
            # Actions to be taken when the trial is completed
            pass  # Placeholder for trial completion logic

        #elif state == States.TrialControl:
        # Increment the trial number counter in the TrialControl state
        # ... existing TrialControl logic ...

        elif state == States.TrialAbort:
         print("IN TRIAL ABORT")
         pass

        elif state == States.DecisionAbort:
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            pass  # Placeholder for DecisionAbort logic

        elif state == States.CenterReward:
            self.center_var = True
            self.center_cnt += 1
            self.reward_manager.deliver_reward('dd', 8, self.punishment_time)
            self.reward_manager.deliver_reward('dd', 11, self.punishment_time)



        elif state == States.TrialAbort:
            # Log that the trial has been aborted
            print("Trial has been aborted.")  # Or use a logging mechanism if available
            trial_validity = 0
            # Update the logger with the aborted trial information
            self.trial_logger.log_trial_data(
                trial_number=self.numcompletedtrial,
                trial_validity=trial_validity,
                opponent_choice="N/A",
                mouse_choice="N/A",
                mouse_reward="-",
                opponent_reward="-"
            )



        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            trialcompleted = True

        return trialcompleted



    def start_streaming_exp(self, num_trial, duration, time_decision, opponent_type, opponent_strategy):
            # OPEN CSV TO LOG DETAILS
            print("opponent ", opponent_type)
            print("opponent strat ", opponent_strategy)
            if opponent_type == "mouse and mouse":
                mouse1 = self.mouse1
                mouse2 = self.mouse2
            elif opponent_type == "mouse and computer":
                mouse1 = self.mouse1
                mouse2 = self.opponent2
            else:
                mouse1 = self.opponent1
                mouse2 = self.opponent2

            self.stateManager.SetTimeOuts(duration, time_decision)
            self.opponent1.SetStrategy(opponent_strategy)
            numcompletedtrial = 0

            currentstate = States.Start
            self.StateActivity(currentstate)
            mouselocation = None
            state_history = []

            while numcompletedtrial < num_trial:
                print(f"Current State: {currentstate}")
                state_history.append(currentstate)
                trialevents = 0

                mouselocation = self.mouse_location_queue_1.get()
                opponent_choice = self.mouse_location_queue_2.get()
                print("mouse 1 location queue", mouselocation)
                print("mouse 2 location queue", opponent_choice)

                # Determine events based on mouse locations
                if mouselocation == [1, 0, 0]:  # Cooperate
                    trialevents += Events.Mouse1Cooporated.value
                elif mouselocation == [0, 1, 0]:  # Center
                    trialevents += Events.Mouse1InCenter.value
                elif mouselocation == [0, 0, 1]:  # Defect
                    trialevents += Events.Mouse1Defected.value


                if opponent_choice == [1, 0, 0]:  # Cooperate
                    trialevents += Events.Mouse2Cooporated.value
                elif opponent_choice == [0, 1, 0]:  # Center
                    trialevents += Events.Mouse2InCenter.value
                elif opponent_choice == [0, 0, 1]:  # Defect
                    trialevents += Events.Mouse2Defected.value


                print("trial events", trialevents)
                nextstate = self.stateManager.DetermineState(trialevents)
                #print("next_state", nextstate)

                if nextstate != currentstate:
                    currentstate = nextstate
                    trialcompleted = self.StateActivity(currentstate)
                    if trialcompleted:
                        break

            #if cv2.waitKey(1) & 0xFF == ord('q'):
             #   break
