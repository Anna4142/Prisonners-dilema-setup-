import time
from enum import Enum
from StateManager import StateManager

##### main
allStateEevents = 0
stateManager = StateManager()
stateManager.SetTimeOut(15, 15)

while allStateEevents != -1:
    opcodestr = input("Enter all-evenets-value [-1 for exit]: ")
    allStateEevents = int(opcodestr)

    if allStateEevents == -1:
        print("Program terminated")
    else:
        currentState = stateManager.DetermineState(allStateEevents)
        print("current state = ", currentState)

