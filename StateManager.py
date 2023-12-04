import time
from enum import Enum

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
    RewardDelivered  = 128

class StateManager:
    def __init__(self):
        self.NextState = {
            States.Start : [States.CenterReward],
            States.CenterReward : [States.TrialStarted],
            States.TrialStarted : [States.M1CM2C, States.M1CM2D, States.M1DM2C, States.M1DM2D],
            States.M1CM2C : [States.WaitForReturn],
            States.M1CM2D: [States.WaitForReturn],
            States.M1DM2C: [States.WaitForReturn],
            States.M1DM2D: [States.WaitForReturn],
            States.WaitForReturn:[States.TrialCompleted],
            States.TrialCompleted:[States.End],
            States.TrialAbort:[States.End, States.TrialStarted],
            States.DecisionAbort:[States.End],
            States.End:[States.End]
        }

        self.TransitionEvent = {
            States.Start : [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.CenterReward : [Events.RewardDelivered.value],
            States.TrialStarted : [Events.Mouse1Cooporated.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Cooporated.value + Events.Mouse2Defected.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Defected.value],
            States.M1CM2C : [Events.RewardDelivered.value],
            States.M1CM2D: [Events.RewardDelivered.value],
            States.M1DM2C: [Events.RewardDelivered.value],
            States.M1DM2D: [Events.RewardDelivered.value],
            States.WaitForReturn:[Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.TrialCompleted:[Events.LastTrial.value],
            States.TrialAbort:[Events.LastTrial.value, Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.DecisionAbort:[Events.LastTrial.value],
            States.End:[0]
        }

        self.TimeOutState = {
            States.Start : None,
            States.CenterReward : States.TrialStarted,   # allow for an unconditional (ignore Reward delivered event) transition
            States.TrialStarted : States.DecisionAbort,
            States.M1CM2C: States.WaitForReturn,         # allow for an unconditional (ignore Reward delivered event) transition
            States.M1CM2D: States.WaitForReturn,         # allow for an unconditional (ignore Reward delivered event) transition
            States.M1DM2C: States.WaitForReturn,         # allow for an unconditional (ignore Reward delivered event) transition
            States.M1DM2D: States.WaitForReturn,         # allow for an unconditional (ignore Reward delivered event) transition
            States.WaitForReturn: States.TrialAbort,
            States.TrialCompleted: States.CenterReward,
            States.TrialAbort: None,
            States.DecisionAbort: States.TrialStarted,
            States.End: None
        }

        self.TransitionTimeOut = {
            States.Start: None,
            States.CenterReward: 0,
            States.TrialStarted: 10,    # 10 seconds is a default value. It is replaces by the SetTimeOut functions.
            States.M1CM2C: 0,
            States.M1CM2D: 0,
            States.M1DM2C: 0,
            States.M1DM2D: 0,
            States.WaitForReturn: 10,    # 10 seconds is a default value. It is replaces by the SetTimeOut functions.
            States.TrialCompleted: 0,
            States.TrialAbort: None,
            States.DecisionAbort: 0,
            States.End: None
        }

        self.current_state = States.Start
        self.StateStartTime = time.time()

    def SetTimeOut(self, decision_time, return_time):
        self.TransitionTimeOut[States.TrialStarted] = decision_time
        self.TransitionTimeOut[States.WaitForReturn] = return_time

    def DetermineState(self, events):
        TransitionEvents = self.TransitionEvent[self.current_state]

        # Check and Perform Event base transition
        for i, event in enumerate(TransitionEvents):
            if event & events == event:
                # Transition to the next state based on the event
                self.current_state = self.NextState[self.current_state][i]
                self.StateStartTime = time.time()
                return self.current_state

        # Check and Perform timeout base transition
        if self.TimeOutState[self.current_state]:
            if time.time() - self.StateStartTime > self.TransitionTimeOut[self.current_state]:
                # Transition to the timeout state
                self.current_state = self.TimeOutState[self.current_state]
                self.StateStartTime = time.time()

        return self.current_state



