import tkinter as tk

class Experiment:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Example")

        # Define a StringVar for the radio buttons
        self.selected_option = tk.StringVar(value="none")

        # Define the radio button options
        options = ["Option 1", "Option 2", "Option 3"]
        for option in options:
            radiobutton = tk.Radiobutton(
                self.window, text=option, variable=self.selected_option, value=option
            )
            radiobutton.pack(anchor='w')

        # Button to retrieve the selected radio button value
        submit_button = tk.Button(self.window, text="Submit", command=self.retrieve_choice)
        submit_button.pack()

        self.window.mainloop()

    def retrieve_choice(self):
        # Retrieve the value from StringVar
        chosen_option = self.selected_option.get()
        print("Chosen option:", chosen_option)

# Create an instance of the GUI
gui = Experiment()
