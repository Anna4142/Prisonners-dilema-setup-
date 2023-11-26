
from locations import Locations

import tkinter as tk


from queue import Queue

class VideoAnalyzerStub:
    def __init__(self, root, data_queue):
        self.mouseLocation = [0, 0, 0]  # Initial state with all zeros

        self.root = root
        self.data_queue = data_queue
        self.label = tk.Label(self.root, text="Press an arrow key", font=('Helvetica', 16))
        self.label.pack(pady=20)

        # Bind arrow keys to their respective handler functions
        self.root.bind('<Left>', self.left_key)
        self.root.bind('<Right>', self.right_key)
        self.root.bind('<Down>', self.down_key)
        self.root.bind('<Up>', self.up_key)

    def update_label(self):
        self.label.config(text=f"Mouse Location: {self.mouseLocation}")

    def left_key(self, event):
        self.mouseLocation = [1, 0, 0]  # Cooperate
        self.update_label()
        self.data_queue.put(self.mouseLocation)

    def right_key(self, event):
        self.mouseLocation = [0, 0, 1]  # Defect
        self.update_label()
        self.data_queue.put(self.mouseLocation)

    def down_key(self, event):
        self.mouseLocation = [0, 1, 0]  # Center
        self.update_label()
        self.data_queue.put(self.mouseLocation)

    def up_key(self, event):
        self.mouseLocation = [0, 0, 0]  # Default
        self.update_label()
        self.data_queue.put(self.mouseLocation)

    def get_mouse_location(self):
        # This method might not be necessary if the queue is used for communication
        return self.mouseLocation


#ANUSHKA-CHANGE IN LOCATION KEY DECODING
#Left arrow for Cooperate ([1, 0, 0]),
#Down arrow for Center ([0, 1, 0]),
#Right arrow for Defect ([0, 0, 1]),
#Up arrow for Default ([0, 0, 0]).
