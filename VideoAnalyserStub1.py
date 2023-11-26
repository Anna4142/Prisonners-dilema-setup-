import tkinter as tk
from enum import Enum

# Assuming the Locations class is defined as an Enum
class Locations(Enum):
    Unknown = 0
    Cooperate = 1
    Center = 2
    Defect = 3

class VideoAnalyzerStub:
    def __init__(self, root):
        self.mouseLocation = [0, 0, 0, 0, 0, 0]  # Initial state with all zeros
        self.root = root
        self.label = tk.Label(self.root, text="Choose a location", font=('Helvetica', 16))
        self.label.pack(pady=20)

        # Adding buttons for different states
        self.cooperate_button = tk.Button(self.root, text="Cooperate", command=lambda: self.set_location(Locations.Cooperate))
        self.cooperate_button.pack()

        self.center_button = tk.Button(self.root, text="Center", command=lambda: self.set_location(Locations.Center))
        self.center_button.pack()

        self.defect_button = tk.Button(self.root, text="Defect", command=lambda: self.set_location(Locations.Defect))
        self.defect_button.pack()

    def update_label(self):
        self.label.config(text=f"Mouse Location: {self.mouseLocation}")

    def set_location(self, location):
        # Reset the mouse location array
        self.mouseLocation = [0, 0, 0, 0, 0, 0]

        if location == Locations.Cooperate:
            self.mouseLocation[0] = 1  # Representing Cooperate
        elif location == Locations.Center:
            self.mouseLocation[1] = 1  # Representing Center
        elif location == Locations.Defect:
            self.mouseLocation[2] = 1  # Representing Defect

        self.update_label()

    def get_mouse_location(self):
        return self.mouseLocation
