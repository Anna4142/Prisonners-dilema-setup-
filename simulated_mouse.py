import random
from VideoAnalyzerStub import Video_Analyzer
from MouseMonitor import MouseMonitor

from locations import Locations
import tkinter as tk
class Simulated_mouse:
    def __init__(self):
        self.strategy = "Unconditional Cooperator"
        root = tk.Tk()
        self.video_analyzer_stub = Video_Analyzer()

        self.LastDecision = Locations.Center
        self.p = 0.5  # Default value for probability
        self.mouse_monitor = MouseMonitor(self.video_analyzer_stub, mouse_id=1)
        self.decisionMade = True
        self.rewardReceived=True

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


    def GetMouseLocation(self, mouse_location):
        if not mouse_location:  # If the mouse_location isn't provided, get it from the MouseMonitor
                mouse_location = self.mouse_monitor.get_mouse_location()  ###Aushka-yet to pass if of mouse to get_ouse_location
        list_opp=[0,0,0]
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
                opp_choice = mouse1_location

        if mouse_location == Locations.Cooperate:
            list_opp=[1, 0, 0]
        elif mouse_location == Locations.Center:
            list_opp=[0, 1, 0]
        elif mouse_location == Locations.Defect:
            list_opp=[0, 0, 1]
        else:
            list_opp= [0, 0, 0]
        #print("OPPONENT CHOICE", opp_choice)
        self.LastDecision = opp_choice  # Update the last decision made by the opponent
        return list_opp
