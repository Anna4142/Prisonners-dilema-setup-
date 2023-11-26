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
    TrialControl        = 10
    TrialAbort          = 11
    DecisionAbort       = 12
    End                 = 13

class Events (Enum):
    Mouse1InCenter   = 1
    Mouse2InCenter   = 2
    Mouse1Cooporated = 4
    Mouse2Cooporated = 8
    Mouse1Defected   = 16
    Mouse2Defected   = 32



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
            States.DecisionAbort:[0],
            States.M1CM2C : [0],
            States.M1CM2D: [0],
            States.M1DM2C: [0],
            States.M1DM2D: [0],
            States.WaitForReturn:[Events.Mouse1InCenter.value+Events.Mouse2InCenter.value],

            States.TrialAbort:[0],
            States.TrialCompleted:[0],
            States.End:[0]
        }

            # these are just defaults. There is a Set function for the real values
        self.center_time = 0
        self.trial_time=0
        self.decision_time = self.trial_time - self.center_time
        self.timeInState=0
        self.TransitionTimeOut = {

            States.Start: None,
            States.CenterReward: None,
            States.TrialStarted: self.decision_time,
            States.M1CM2C: None,
            States.M1CM2D: None,
            States.M1DM2C: None,
            States.M1DM2D: None,
            States.WaitForReturn: self.center_time,
            States.TrialCompleted: None,
            States.DecisionAbort:None,
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
            States.DecisionAbort: None,
            States.End: None
        }

        self.current_state = States.Start
        self.StateStartTime = time.time()

    def SetTimeOuts(self, trial_time, center_time):
        self.decision_time = center_time
        ##Anushka-no need for the variable center time
        self.trial_time=trial_time
        self.return_time=self.trial_time-self.decision_time
    '''''
    def DetermineState(self, Events):
        TransitionEvents = self.TransitionEvent[self.current_state]
        timeInState = time.time() - self.StateStartTime

        for i in range(len(TransitionEvents)):
            if TransitionEvents[i] & Events == TransitionEvents[i]:
                self.current_state = self.NextState[self.current_state][i]
                self.StateStartTime = time.time()
                print("CURRENT STATE",self.current_state)
            elif (self.TransitionTimeOut[self.current_state] is not None) and (timeInState > self.TransitionTimeOut[self.current_state]):
                self.current_state = self.TimeOutState[self.current_state]
                self.StateStartTime = time.time()

        return self.current_state
    '''''


    def DetermineState(self, events):
        TransitionEvents = self.TransitionEvent[self.current_state]
        self.timeInState = time.time() - self.StateStartTime
        print("TIME IN STATE",self.timeInState)
        for i, event in enumerate(TransitionEvents):
            if event & events == event:
                self.current_state = self.NextState[self.current_state][i]
                self.StateStartTime = time.time()
                break
        else:  # This else part executes if no break occurs in the loop
            if (self.TransitionTimeOut[self.current_state] is not None) and (self.timeInState > self.TransitionTimeOut[self.current_state]):
                self.current_state = self.TimeOutState[self.current_state]
                self.StateStartTime = time.time()

        return self.current_state



