import time
from vimba import *
from VideoAnalyser1 import Video_Analyzer
#from VideoAnalyzer import Video_Analyzer
#from MouseMonitor import MouseMonitor
from MouseMonitor1 import MouseMonitor
#from VideoAnalyzerStub import Video_Analyzer
from MouseMonitor import Locations
from logger import TrialLogger
from simulated_mouse import Simulated_mouse
from ArduinoDigital import ArduinoDigital
from StateManager import StateManager
from StateManager import States
from StateManager import Events
import experimentgui
from RewardManager import RewardManager
import tkinter as tk
from logger import TrialLogger
#from ArduinoDigitalSim import ArduinoDigital  ##Anushka-new class
class ExperimentManager:
    def __init__(self):
        # Initialize other components here
        self.root = tk.Tk()  # Create a new Tkinter root window if not provided
        #self.videoAnalyser = Video_Analyzer(self.root)
        with Vimba.get_instance() as vimba:
            # Create Video_Analyzer instance with the active Vimba instance
            self.videoAnalyser = Video_Analyzer(vimba)

        #self.videoAnalyser = Video_Analyzer()  # or VideoAnalyzer, ensure correct class name
        self.mouse1 = MouseMonitor(self.videoAnalyser, 1)
        self.mouse2 = MouseMonitor(self.videoAnalyser, 2)
        self.opponent = Simulated_mouse()

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

        ##
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

    def initialize_arduino(self):
        comport="COM11"
        self.board = ArduinoDigital(comport)
        # Set all pins to low
        for pin in [7, 8, 9, 10, 11, 12]:
            self.board.DigitalLow(pin)


    def StateActivity(self, state):
        trialcompleted = False

        if state == States.Start:
            #self.videoAnalyser.stream_and_process()
            pass

        elif state == States.InitialReward:
            # Deliver a center reward as an initial reward
            self.reward_manager.deliver_reward('center', 0, self.center_reward_time)

        elif state == States.M1CM2C:
            # Deliver cooperative rewards to both mice
            self.cc_var = True
            self.cc_cnt += 1
            self.reward_manager.deliver_reward('cc', 1, self.reward_time)
            self.reward_manager.deliver_reward('cc', 2, self.reward_time)

        elif state == States.M1CDM2D:
            # Mouse 1 cooperates, Mouse 2 defects
            self.cd_var = True
            self.cd_cnt += 1
            self.reward_manager.deliver_reward('cd', 1, self.reward_time)
            self.reward_manager.deliver_reward('cd', 2, self.punishment_time)

        elif state == States.M1DCM2C:
            # Mouse 1 defects, Mouse 2 cooperates
            self.dc_var = True
            self.dc_cnt += 1
            self.reward_manager.deliver_reward('dc', 1, self.punishment_time)
            self.reward_manager.deliver_reward('dc', 2, self.reward_time)

        elif state == States.M1DDM2D:
            # Both mice defect
            self.dd_var = True
            self.dd_cnt += 1
            self.reward_manager.deliver_reward('dd', 1, self.punishment_time)
            self.reward_manager.deliver_reward('dd', 2, self.punishment_time)



        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            trialcompleted = True



        return trialcompleted

    def start_streaming_exp(self, num_trial, duration, time_decision, opponent_type, opponent_strategy):
        # OPEN CSV TO LOG DETAILS
        if opponent_type == "mouse and mouse":
            mouse1 = self.mouse1
            mouse2 = self.mouse2
        elif opponent_type == "mouse and computer":
            mouse1 = self.mouse1
            mouse2 = self.opponent
        else:
            mouse1 = self.opponent
            mouse2 = self.opponent
        currentstate=self.stateManager.SetTimeOuts(duration, time_decision)  ##Anushka-made some changes for functionality
        self.opponent.SetStrategy(opponent_strategy)
        numcompletedtrial = 0

        self.StateActivity(States.Start)  # start state activities for first trial
        mouselocation = None

        while numcompletedtrial < num_trial:

            trialevents = 0;
            zone_activations = self.videoAnalyser.process_single_frame()
            print("zone activations",zone_activations)
            mouselocation = self.mouse1.get_mouse_location(zone_activations)
            opponent_choice = self.mouse2.get_mouse_location(zone_activations)
            if mouselocation == Locations.Center:
                trialevents = trialevents + Events.Mouse1InCenter
            elif mouselocation == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse1Cooporated
            elif mouselocation == Locations.Defect:
                trialevents = trialevents + Events.Mouse1Defected


            if opponent_choice == Locations.Center:
                trialevents = trialevents + Events.Mouse2InCenter
            elif opponent_choice == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse2Cooporated
            elif opponent_choice == Locations.Defect:
                trialevents = trialevents + Events.Mouse2Defected

            nextstate = self.stateManager.DetermineState(trialevents)

            if nextstate != currentstate:
                currentstate = nextstate
                trialcompleted = self.StateActivity(currentstate)

            numcompletedtrial = numcompletedtrial + 1
                # Assuming you have collected the necessary data for each trial
            trial_number = numcompletedtrial   # Adjust as needed
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

            # Ensure that all required arguments are provided
            #TrialLogger.log_trial_data(trial_number, trial_validity, opponent_choice, mouse_choice, mouse_reward,opponent_reward)#####CORRECT ERROR



            #if cv2.waitKey(1) & 0xFF == ord('q'):
             #   break
