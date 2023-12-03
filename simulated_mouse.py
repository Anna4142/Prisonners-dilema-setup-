import random

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

    def get_mouse_location(self, zones_list, other_mouse_location):
        if self.decisionMade:
            if self.rewardReceived:
                opp_choice = Locations.Center
            else:
                opp_choice = self.LastDecision
        else:
            self.decisionMade = True

            if self.strategy == "Unconditional Cooperator":
                opp_choice = Locations.Cooperate
            elif self.strategy == "Unconditional Defector":
                opp_choice = Locations.Defect
            elif self.strategy == "Random":
                opp_choice = random.choice([Locations.Cooperate, Locations.Defect])
            elif self.strategy == "Probability p Cooperator":
                if random.random() < self.p:
                    opp_choice = Locations.Cooperate
                else:
                    opp_choice = Locations.Defect
            elif self.strategy == "Tit for Tat":
                opp_choice = other_mouse_location

        self.LastDecision = opp_choice  # Update the last decision made by the opponent
        return opp_choice
