import random
from StateManager import States
from locations import Locations

class Simulated_mouse:
    def __init__(self):
        self.strategy = "Unconditional Cooperator"
        self.LastDecision = Locations.Center
        self.p = 0.5  # Default value for probability
        self.decisionMade = True
        self.rewardReceived = True

    def SetStrategy(self, strategy):
        self.strategy = strategy

    def NewTrial(self):
        self.decisionMade = False
        self.rewardReceived = False

    def setRewardReceived(self):
        self.rewardReceived = True

    def setProbability(self, p):
        """Method to set the probability value for 'Probability p Cooperator' strategy"""
        if 0 <= p <= 1:
            self.p = p
        else:
            print("Error: p should be between 0 and 1")

    def get_mouse_location(self, mouse_location,current_state):
        list_opp = Locations.Unknown  # Default to no decision
        if not mouse_location:  # If the mouse_location isn't provided, get it from the MouseMonitor
                mouse_location = self.mouse_monitor.get_mouse_location()
        if current_state == States.Start:
            list_opp = Locations.Center

        elif current_state == States.CenterReward:
            list_opp = Locations.Center

        elif current_state == States.TrialStarted:
            # Decision-making based on the strategy
            # Existing logic based on strategy goes here

            if self.strategy == "Unconditional Cooperator":
                list_opp =Locations.Cooperate # Cooperate in these states

            elif self.strategy == "Unconditional Defector":
                list_opp = Locations.Defect  # Defect in these states

            elif self.strategy == "Random":
                list_opp = random.choice([Locations.Cooperate,  Locations.Defect ])  # Randomly choose between Cooperate and Defect

            elif self.strategy == "Probability p Cooperator":
                list_opp = Locations.Cooperate if random.random() < self.p else Locations.Defect  # Cooperate based on probability p

            elif self.strategy == "Tit for Tat":
                # Tit for Tat strategy: Cooperate if opponent cooperated, otherwise defect
                list_opp = mouse_location


        elif current_state == States.M1CM2C:
           pass  # Example: Cooperate

        elif current_state == States.M1CM2D:
            pass # Example: Cooperate

        elif current_state == States.M1DM2C:
            pass  # Example: Defect

        elif current_state == States.M1DM2D:
           pass # Example: Defect

        elif current_state == States.WaitForReturn:
            list_opp = Locations.Center   # Example: Move to Center

        elif current_state == States.TrialCompleted:
            list_opp = Locations.Center
        elif current_state == States.TrialAbort:
            list_opp = Locations.Center

        elif current_state == States.DecisionAbort:
            list_opp =Locations.Center
        elif current_state == States.End:
            list_opp = Locations.Center

        return list_opp