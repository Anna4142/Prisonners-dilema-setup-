import time
from enum import Enum

class States(Enum):
    WaitForStart        = 1
    Start               = 2
    CenterReward        = 3
    TrialStarted        = 4
    M1CM2C              = 5
    M1CM2D              = 6
    M1DM2C              = 7
    M1DM2D              = 8
    WaitForReturn       = 9
    TrialCompleted      = 10
    TrialAbort          = 11
    DecisionAbort       = 12
    End                 = 13

class Events(Enum):
    StartTrial        = 1
    Mouse1InCenter    = 2
    Mouse2InCenter    = 4
    Mouse1Cooporated  = 8
    Mouse2Cooporated  = 16
    Mouse1Defected    = 32
    Mouse2Defected    = 64
    LastTrial         = 128
    RewardDelivered   = 256


class StateManager:
    def __init__(self):
        self.NextState = {
            States.WaitForStart : [States.Start]
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

            States.WaitForStart: [Events.StartTrial.value]#move ur hand to the center of the maze after you are done putting the mice
            States.Start : [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.CenterReward : [0],
            States.TrialStarted : [Events.Mouse1Cooporated.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Cooporated.value + Events.Mouse2Defected.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Cooporated.value,
                                   Events.Mouse1Defected.value + Events.Mouse2Defected.value],
            States.M1CM2C : [0],
            States.M1CM2D: [0],
            States.M1DM2C: [0],
            States.M1DM2D: [0],
            States.WaitForReturn:[Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.TrialCompleted:[Events.LastTrial.value],
            States.TrialAbort:[Events.LastTrial.value, Events.Mouse1InCenter.value + Events.Mouse2InCenter.value],
            States.DecisionAbort:[Events.LastTrial.value],
            States.End:[0]
        }

        self.TimeOutState = {
            States.WaitForStart :None
            States.Start : None,
            States.CenterReward : None,
            States.TrialStarted : States.DecisionAbort,
            States.M1CM2C: None,
            States.M1CM2D: None,
            States.M1DM2C: None,
            States.M1DM2D: None,
            States.WaitForReturn: States.TrialAbort,
            States.TrialCompleted: States.CenterReward,
            States.TrialAbort: None,
            States.DecisionAbort: States.TrialStarted,
            States.End: None
        }

        # the time out setting are just defaults
        self.decision_time = 0
        self.return_time = 0

        self.TransitionTimeOut = {
            States.WaitForStart :None
            States.Start: None,
            States.CenterReward: None,
            States.TrialStarted: self.decision_time,
            States.M1CM2C: None,
            States.M1CM2D: None,
            States.M1DM2C: None,
            States.M1DM2D: None,
            States.WaitForReturn: self.return_time,
            States.TrialCompleted: 0,
            States.TrialAbort: None,
            States.DecisionAbort: 0,
            States.End: None
        }

        self.current_state = States.Start
        self.StateStartTime = time.time()

    def SetTimeOuts(self, decision_time, return_time):
        self.decision_time = decision_time
        self.return_time = return_time

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