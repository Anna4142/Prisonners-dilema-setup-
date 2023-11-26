from enum import Enum

class Locations(Enum):
    Unknown = [0,0,0]
    Cooperate = [1,0,0]
    Center = [0,1,0]
    Defect = [0,0,1]
