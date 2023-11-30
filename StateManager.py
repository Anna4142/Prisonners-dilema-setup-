import time
from enum import Enum
from timer_state_transition import StateTimer
class States (Enum):
    Start               = 1
    CenterReward        = 2
    TrialStarted        = 3
    M1CM2C              = 4
    M1CM2D              = 5
    M1DM2C              = 6
    M1DM2D              = 7
    WaitForReturn       = 8
    TrialCompleted      = 9
    TrialAbort          = 10
    DecisionAbort       = 11
    End                 = 12

class Events (Enum):
    Mouse1InCenter   = 1
    Mouse2InCenter   = 2
    Mouse1Cooporated = 4
    Mouse2Cooporated = 8
    Mouse1Defected   = 16
    Mouse2Defected   = 32

    LastTrial        = 64


class StateManager:
    def __init__(self):
        self.NextState = {
            States.Start : [States.CenterReward],
            States.CenterReward : [States.TrialStarted],
            States.TrialStarted : [States.M1CM2C, States.M1CM2D, States.M1DM2C, States.M1DM2D,States.DecisionAbort],
            States.DecisionAbort:[States.TrialStarted,States.End],
            States.M1CM2C : [States.WaitForReturn],
            States.M1CM2D: [States.WaitForReturn],
            States.M1DM2C: [States.WaitForReturn],
            States.M1DM2D: [States.WaitForReturn],
            States.WaitForReturn:[States.TrialCompleted,States.TrialAbort],

            States.TrialCompleted:[States.CenterReward,States.End],
            States.TrialAbort:[States.TrialStarted,States.End]
        }

        self.TransitionEvent = {
            States.Start : [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.CenterReward : [0],
            States.TrialStarted : [Events.Mouse1Cooporated.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Cooporated.value + Events.Mouse2Defected.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Defected.value],
            States.DecisionAbort:[0,Events.LastTrial],
            States.M1CM2C : [0],
            States.M1CM2D: [0],
            States.M1DM2C: [0],
            States.M1DM2D: [0],
            States.WaitForReturn:[Events.Mouse1InCenter.value+Events.Mouse2InCenter.value],

            States.TrialAbort:[Events.Mouse1InCenter.value + Events.Mouse2InCenter.value,Events.LastTrial],
            States.TrialCompleted:[0,Events.LastTrial],
            States.End:[0]
        }



        def SetTimeOuts(self, trial_time, decision_time):
            self.decision_time = decision_time
            ##Anushka-no need for the variable center time
            self.trial_time = trial_time
            self.return_time = self.trial_time - self.decision_time
            # Initialize state timers
        self.TransitionTimeOut = {

                States.Start: None,
                States.CenterReward: None,
                States.TrialStarted: StateTimer(self.decision_time),
                States.M1CM2C: None,
                States.M1CM2D: None,
                States.M1DM2C: None,
                States.M1DM2D: None,
                States.WaitForReturn: StateTimer(self.return_time),
                States.TrialCompleted: None,
                States.DecisionAbort: None,
                States.TrialAbort: None,
                States.End: None
        }


        self.TimeOutState = {
            States.Start : None,
            States.CenterReward : None,
            States.TrialStarted : States.DecisionAbort,

            States.M1CM2C: None,
            States.M1CM2D: None,
            States.M1DM2C: None,
            States.M1DM2D: None,
            States.WaitForReturn: States.TrialAbort,
            States.TrialCompleted: None,
            #States.TrialControl: States.TrialStarted,
            States.TrialAbort: None,
            States.DecisionAbort: States.TrialStarted,
            States.End: None
        }

        self.current_state = States.Start
        self.StateStartTime = time.time()

    def DetermineState(self, events):
        TransitionEvents = self.TransitionEvent[self.current_state]

        for i, event in enumerate(TransitionEvents):
            if event & events == event:
                # Transition to the next state based on the event
                new_state = self.NextState[self.current_state][i]

                # Manage timers for the new state
                if new_state in self.TransitionTimeOut and self.TransitionTimeOut[new_state]:
                    self.TransitionTimeOut[new_state].reset()

                # Stop the timer of the current state if it's not needed in the new state
                if self.current_state in self.TransitionTimeOut and self.TransitionTimeOut[self.current_state]:
                    self.TransitionTimeOut[self.current_state].stop()

                # Update the current state and state start time
                self.current_state = new_state
                self.StateStartTime = time.time()
                return self.current_state

        # Check timer for the current state
        if self.current_state in self.TransitionTimeOut and self.TransitionTimeOut[self.current_state]:
            timer = self.TransitionTimeOut[self.current_state]
            if timer.is_done():
                # Transition to the timeout state
                new_state = self.TimeOutState[self.current_state]
                timer.reset()  # Reset the timer for future use
                self.current_state = new_state
                self.StateStartTime = time.time()

        return self.current_state



