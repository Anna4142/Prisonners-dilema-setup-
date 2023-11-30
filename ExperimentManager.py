#from VideoAnalyzer import VideoAnalyzer
from VideoAnalyzerSim import VideoAnalyzer     # Simulated vs HW-based versions of the VideoAnalyzer

#from ArduinoDigital import ArduinoDigital
from ArduinoDigitalSim import ArduinoDigital   # Simulated vs HW-based versions of the VideoAnalyzer

from MouseMonitor import MouseMonitor
from locations import Locations
from logger import TrialLogger
from simulated_mouse import Simulated_mouse
from StateManager import StateManager
from StateManager import States
from StateManager import Events
from RewardManager import RewardManager

from datetime import datetime


class ExperimentManager:
    def __init__(self):
        # Initialize other components here
        self.videoAnalyser = VideoAnalyzer()

        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%y%m%d%H%M%S")
        self.trial_logger = TrialLogger("./../ExperimentLogFiles/PrisonerDilemmaPy_" + dt_string)
        self.numcompletedtrial = 0
        self.stateManager = StateManager()

        # Set default reward and punishment times
        self.reward_time = 0.02
        self.sucker_time = 0
        self.temptation_time = 0.009
        self.punishment_time = 0.004
        self.center_reward_time = 0.1

        ### VARIABLES FOR LOG FILE INITIALLY INITIALIZED TO FALSE
        self.opponent_choice = "N/A",
        self.mouse_choice = "N/A",
        self.mouse_reward = "-",
        self.opponent_reward = "-"
        self.cc_cnt = 0
        self.cd_cnt = 0
        self.dc_cnt = 0
        self.dd_cnt = 0
        self.center_cnt = 0

        # Initialize Arduino board and reward delivery system
        self.board = ArduinoDigital("COM5")
        self.reward_manager = RewardManager(self.board, [7, 8, 9, 10, 11, 12])

    def StateActivity(self, state, mouse1simulated, mouse2simulated):
        ExperimentCompleted = False

        if state == States.Start:
            # Initialize variables, set some flags, start recording, etc.
            pass

        elif state == States.CenterReward:
            self.center_var = True
            self.center_cnt += 1
            if not mouse1simulated:
                self.reward_manager.deliver_reward('dd', 8, self.punishment_time)
            if not mouse2simulated:
                self.reward_manager.deliver_reward('dd', 11, self.punishment_time)

        elif state == States.TrialStarted:
            if mouse1simulated:
                mouse1simulated.NewTrial()
            if mouse2simulated:
                mouse2simulated.NewTrial()

        elif state == States.M1CM2C:
            # Actions for M1CM2C state
            self.mouse_choice = "C"
            self.opponent_choice = "C"
            self.mouse_reward = "12ml"
            self.opponent_reward = "12ml"
            self.cc_cnt += 1

            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cc', 12, self.reward_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cc', 7, self.reward_time)

        elif state == States.M1CM2D:
            # Actions for M1CDM2D state
            self.mouse_choice = "C"
            self.opponent_choice = "D"
            self.mouse_reward = "0ml"
            self.opponent_reward = "15ml"
            self.cd_cnt += 1
            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cd', 12, self.reward_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('cd', 9, self.punishment_time)

        elif state == States.M1DM2C:
            # Actions for M1DCM2C state
            self.mouse_choice = "D"
            self.opponent_choice = "C"
            self.mouse_reward ="15ml"
            self.opponent_reward ="0ml"
            self.dc_cnt += 1
            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dc', 10, self.punishment_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dc', 7, self.reward_time)

        elif state == States.M1DM2D:
            # Actions for M1DDM2D state
            self.mouse_choice = "D"
            self.opponent_choice = "D"
            self.mouse_reward = "15ml"
            self.opponent_reward = "15ml"
            self.dd_cnt += 1
            if mouse1simulated:
                mouse1simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dd', 10, self.punishment_time)
            if mouse2simulated:
                mouse2simulated.setRewardReceived()
            else:
                self.reward_manager.deliver_reward('dd', 9, self.punishment_time)

        elif state == States.WaitForReturn:
            # Handle WaitForReturn state
            pass  # Placeholder for WaitForReturn logic

        elif state == States.TrialCompleted:
            # Increment the trial number counter
            self.numcompletedtrial += 1
            print("Trial Completed. Number of completed trials: ", self.numcompletedtrial)
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Completed Trial", self.opponent_choice, self.mouse_choice,
                                             self.mouse_reward, self.opponent_reward)

        elif state == States.TrialAbort:
            # Log that the trial has been aborted
            print("Trial has been aborted.")  # Or use a logging mechanism if available
            self.opponent_choice = "N/A",
            self.mouse_choice = "N/A",
            self.mouse_reward = "-",
            self.opponent_reward = "-"
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Return Abort", self.opponent_choice, self.mouse_choice,
                                             self.mouse_reward, self.opponent_reward)

        elif state == States.DecisionAbort:
            # Handle DecisionAbort state
            print("IN DECISION ABORT")
            self.opponent_choice = "N/A",
            self.mouse_choice = "N/A",
            self.mouse_reward = "-",
            self.opponent_reward = "-"
            self.trial_logger.log_trial_data(self.numcompletedtrial, "Decision Abort", self.opponent_choice, self.mouse_choice,
                                             self.mouse_reward, self.opponent_reward)

        elif state == States.End:
            # Stop recording, finalize logs, show end message, etc.
            ExperimentCompleted = True

        return ExperimentCompleted


    def start_streaming_exp(self, num_trial, duration, time_decision, opponent_type, opponent_strategy):
        print("opponent ", opponent_type)
        print("opponent strat ", opponent_strategy)

        if opponent_type == "mouse and mouse":
            mouse1 = MouseMonitor(self.videoAnalyser, 1)
            mouse1sim = None
            mouse2 = MouseMonitor(self.videoAnalyser, 2)
            mouse2sim = None
        elif opponent_type == "mouse and computer":
            mouse1 = MouseMonitor(self.videoAnalyser, 1)
            mouse1sim = None
            mouse2 = Simulated_mouse()
            mouse2.SetStrategy(opponent_strategy)
            mouse2sim = mouse2
        else:
            mouse1 = Simulated_mouse()
            mouse1.SetStrategy(opponent_strategy)
            mouse1sim = mouse1
            mouse2 = Simulated_mouse()
            mouse2.SetStrategy(opponent_strategy)   #Micky - the case of two different strategies for two simulated mice is not handled
            mouse2sim = mouse2

        self.stateManager.SetTimeOuts(duration, time_decision)

        currentstate = None
        mouse1location = None
        mouse2location = None

        while currentstate != States.End:
            trialevents = 0;

            if self.numcompletedtrial == self.num_trial:
                trialevents += Events.LastTrial.value
                print("TRIAL COMPLETE EVENTS", trialevents)
            else:
                mouse1location = mouse1.GetMouseLocation(mouse2location)
                mouse2location = mouse2.GetMouseLocation(mouse1location)

                if mouse1location == Locations.Center:
                    trialevents += Events.Mouse1InCenter.value
                elif mouse1location == Locations.Cooperate:
                    trialevents += Events.Mouse1Cooporated.value
                elif mouse1location == Locations.Defect:
                    trialevents += Events.Mouse1Defected.value

                if mouse2location == Locations.Center:
                    trialevents += Events.Mouse2InCenter.value
                elif mouse2location == Locations.Cooperate:
                    trialevents += Events.Mouse2Cooporated.value
                elif mouse2location == Locations.Defect:
                    trialevents += Events.Mouse2Defected.value

            nextstate = self.stateManager.DetermineState(trialevents)

            if nextstate != currentstate:
                currentstate = nextstate
                self.StateActivity(currentstate, mouse1sim, mouse2sim)
                print(f"next State: {nextstate}")