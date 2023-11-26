import time

from VideoAnalyzer import VideoAnalyzer
from MouseMonitor import MouseMonitor
from MouseMonitor2 import MouseMonitor
from MouseMonitor import Locations
from MouseMonitor2 import Locations
from Opponent import Opponent
from ArduinoDigital import ArduinoDigital
from StateManager import StateManager
from StateManager import States
from StateManager import Events
import experimentgui


class ExperimentManager:
    def __init__(self):
        # Initialize other components here

        #self.videoAnalyser = VideoAnalyzer()
        self.VideoAnalyzer = VideoAnalyzerStub()               # Micky: I created this module for debug purposes.
                                                               #        This model uses keyboard arrows to signal where the mouse is.
                                                               #        this way we can debug the whole system without mice and video.
                                                               #        once we are happy with the logic we can add HW and animals

        self.mouse1 = MouseMonitor(self.videoAnalyser)         # Micky: You do not need two MouseMonitor Classes. Only one that gets the mouse ID
                                                               #        It Should monitor as a parameter to the __init__ function.
                                                               #        Somthing like Mouse1 = MouseMonitor("North_Mouse")
        self.mouse2 = MouseMonitor2(self.videoAnalyser)        #        Although this will work, I think you should create only two mice objects
                                                               #        of the correct type in the start_streaming_exp()
        self.opponent = Opponent()                             #        I suggest to change the class name to MouseSim or ComputerMouse or somthing

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
        self.initialize_csv_logging()
        self.initialize_video_capture()

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

    def initialize_arduino(self):
        self.board = ArduinoDigital()
        # Set all pins to low
        for pin in [7, 8, 9, 10, 11, 12]:
            self.board.DigitalLow(pin)

    def deliver_cc(self, reward_time):
        self.board.DigitalHigh(12)
        time.sleep(reward_time)
        self.board.DigitalLow(12)
        self.board.DigitalHigh(7)
        time.sleep(reward_time)
        self.board.DigitalLow(7)

    def deliver_cd(self, temp_time, punishment_time):
        self.board.DigitalHigh(12)
        time.sleep(punishment_time)
        self.board.DigitalLow(12)
        self.board.DigitalHigh(9)
        time.sleep(temp_time)
        self.board.DigitalLow(9)

    def deliver_dc(self, temp_time, punishment_time):
        self.board.DigitalHigh(10)
        time.sleep(temp_time)
        self.board.DigitalLow(10)
        self.board.DigitalHigh(7)
        time.sleep(punishment_time)
        self.board.DigitalLow(7)

    def deliver_dd(self, sucker_time):
        self.board.DigitalHigh(10)
        time.sleep(sucker_time)
        self.board.DigitalLow(10)
        self.board.DigitalHigh(11)
        time.sleep(sucker_time)
        self.board.DigitalLow(11)

    def deliver_center(self, center_reward_time):
        self.board.DigitalHigh(11)
        time.sleep(center_reward_time)
        self.board.DigitalLow(11)
        self.board.DigitalHigh(8)
        time.sleep(center_reward_time)
        self.board.DigitalLow(8)

    def StateAtivity(self, state):
        trialcompleted = False

        if state == States.Start:
            # Example: Initialize variables, set some flags, start recording, etc.
            pass

        elif state == States.InitialReward:
            # Deliver a center reward as an initial reward
            self.deliver_center(self.center_reward_time)

        elif state == States.TrialStarted:
            # Start a timer, log the start of the trial, etc.
            pass

        elif state == States.M1CM2C:
            # Deliver cooperative rewards to both mice
            self.cc_var = True
            self.cc_cnt += 1
            self.deliver_cc(self.reward_time)

        elif state == States.M1CM2D:
            # M1 cooperates but M2 defects
            self.cd_var = True
            self.cd_cnt += 1
            self.deliver_cd(self.temptation_time, self.punishment_time)

        elif state == States.M1DM2C:
            # M1 defects but M2 cooperates
            self.dc_var = True
            self.dc_cnt += 1
            self.deliver_dc(self.temptation_time, self.punishment_time)

        elif state == States.M1DM2D:
            # Both M1 and M2 defect
            self.dd_var = True
            self.dd_cnt += 1
            self.deliver_dd(self.sucker_time)

        elif state == States.WaitForReturn:
            # Example: Wait for mouse to return to a specific zone.
            pass

        elif state == States.PostDecisionCenter:
            # Analyze decisions made and prepare for next phase.
            pass

        elif state == States.TrialControl:
            # Example: Write to CSV logging
            """""
            log csv data
            self.csv_writer.writerow([current_time,'TrialControl Event'])  
            self.csv_file.flush()
            
            """

        elif state == States.TrialAbort:

            trialcompleted = True

        elif state == States.End:
            # Example: Stop recording, finalize logs, show end message, etc.
            trialcompleted = True

        return trialcompleted

    def start_streaming_exp(self, num_trial, duration, time_decision, opponent_type, opponent_strategy):
        # OPEN CSV TO LOG DETAILS
        if opponent_type == "mouse and mouse":
            mouse1 = self.mouse1                    #Micky: Create the mice object hear rather than in the __init__ function
            mouse2 = self.mouse2
        elif opponent_type == "mouse and computer":
            mouse1 = self.mouse1
            mouse2 = self.opponent
        else:
            mouse1 = self.opponent                  #Micky: Is there really a nead for this mode?
            mouse2 = self.opponent

        self.stateManager.SetTimeOuts(time_decision, center_reward_time)
        self.opponet.SetStrategy(opponent_strategy)   #Micky: This should be moved to were the opponent is created. and use Mosue2 not opponent
                                                      #       I recomand not to have an opponent variable at all. Its not neeed.
        numcompletedtrial = 0
        currentstate = States.Start                   #Micky: It make more sense to get the currentState from the state manager rather
                                                      #       initialze it here independently

        self.StateAtivity(States.Start)  # start state activities for first trial #Micky: Use currentstate not States.Start explicitly.

        mouselocation=None
        while numcompletedtrial < num_trial:

            trialevents = 0;

            mouselocation = mouse1.GetMouseLocation(mouselocation)
            if mouselocation == Locations.Center:
                trialevents = trialevents + Events.Mouse1InCenter
            elif mouselocation == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse1Cooporated
            elif mouselocation == Locations.Defect:
                trialevents = trialevents + Events.Mouse1Defected

            opponent_choice = mouse2.GetMouseLocation(mouselocation)
            if opponent_choice == Locations.Center:
                trialevents = trialevents + Events.Mouse2InCenter
            elif opponent_choice == Locations.Cooperate:
                trialevents = trialevents + Events.Mouse2Cooporated
            elif opponent_choice == Locations.Defect:
                trialevents = trialevents + Events.Mouse2Defected

                                                    # Micky: add a call the reward manager to see if reward delivered
                                                    #        if reward delivered set an addtional event bit
                                                    #        trialevents = trialevents + Events.RewardDelivered
                                                    #        this event is already in the state diagram but not in the
                                                    #        state manager code. You need to add it and update all the
                                                    #        transition tables.

            nextstate = self.stateManager.statemanager.DetermineState(trialevents)

            if nextstate != currentstate:
                currentstate = nextstate
                trialcompleted = self.StateAtivity(curretstate)

            if trialcompleted:
                numcompletedtrial = numcompletedtrial + 1

            if cv2.waitKey(1) & 0xFF == ord('q'):    # Micky: I suggest using if keyboard.is_pressed('q') instead of the cv2 function.
                                                     # Micky: this way cv2 is only used in the video analyzer
                                                     #        by replacing the video analyzerand we will be able to test
                                                     #        by a simulation module (I will explein next time) we will be able to test the complete logic
                                                     #        of the software without the lab HW (or mice)
                break
