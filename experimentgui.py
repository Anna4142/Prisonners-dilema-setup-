import tkinter as tk
from tkinter import messagebox


class ExperimentGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prisoner's Dilemma Experiment")
        self.num_trials_entry = tk.StringVar(value=None)
        self.trial_duration_entry = tk.StringVar(value=None)
        self.decision_time_entry = tk.StringVar(value=None)
        self.selected_opp = tk.StringVar(value=None)
        # Initialize variables
        self.selected_opp = tk.StringVar(value=None)
        self.strategy_option_widgets = []  # Initialize an empty list to keep track of strategy option widgets
        self.selected_opponent_type = None
        # Setup the GUI components


    def setup_gui(self):
        # Opponent options

        # Entry fields for trials, duration, etc.
        self.create_input_fields()
        self.create_opp_options()
        # Create a button to start the experiment and disable it initially
        self.start_button = tk.Button(self.window, text="Start Experiment", command=self.start_experiment, state='disabled')
        self.start_button.pack(pady=20)
        self.window.mainloop()

    def create_opp_options(self):
        # Create opponent selection radio buttons
        tk.Label(self.window, text="Select the opponent:").pack(anchor='w', padx=20, pady=10)
        self.selected_opp.set("none")
        opp_options = [
            ("Mouse and Mouse", "mouse_mouse"),
            ("Mouse and Computer", "mouse_computer"),
            ("Computer and Computer", "computer_computer")
        ]

        for text, mode in opp_options:
            radiobutton = tk.Radiobutton(
                self.window, text=text, variable=self.selected_opp, value=mode,
                command=self.update_strategy_options
            )
            radiobutton.pack(anchor='w', padx=20, pady=5)

    def create_input_fields(self):
        # Create and pack a label and entry for number of trials
        tk.Label(self.window, text="Number of Trials:").pack(anchor='w', padx=20, pady=5)
        self.num_trials_var = tk.StringVar()  # StringVar for number of trials
        self.num_trials_entry = tk.Entry(self.window, textvariable=self.num_trials_var)
        self.num_trials_entry.pack(anchor='w', padx=20, pady=5)

        # Create and pack a label and entry for trial duration
        tk.Label(self.window, text="Trial Duration (seconds):").pack(anchor='w', padx=20, pady=5)
        self.trial_duration_var = tk.StringVar()  # StringVar for trial duration
        self.trial_duration_entry = tk.Entry(self.window, textvariable=self.trial_duration_var)
        self.trial_duration_entry.pack(anchor='w', padx=20, pady=5)

        # Create and pack a label and entry for decision time
        tk.Label(self.window, text="Decision Time (seconds):").pack(anchor='w', padx=20, pady=5)
        self.decision_time_var = tk.StringVar()  # StringVar for decision time
        self.decision_time_entry = tk.Entry(self.window, textvariable=self.decision_time_var)
        self.decision_time_entry.pack(anchor='w', padx=20, pady=5)

    def update_strategy_options(self):
        # Remove previous strategy options if they exist
        self.destroy_strategy_options()

        # Based on the opponent selected, either show the start button or create strategy options
        if self.selected_opp.get() == "mouse_mouse":
            # No strategy options needed for mouse vs. mouse, enable start button
            self.start_button['state'] = 'normal'
        elif self.selected_opp.get() == "mouse_computer" or self.selected_opp.get() == "computer_computer":
            # Create strategy options for the computer opponent(s)
            # For mouse_computer, create strategy options for the computer
            # For computer_computer, create strategy options for both computers
            self.create_strategy_options()

    def create_strategy_options(self):
        # Check if it's a single computer or two computers
        if self.selected_opp.get() == "mouse_computer":
            # Create strategy options for the computer
            self.create_strategy_option("Computer's Strategy:", "strategy1")
        elif self.selected_opp.get() == "computer_computer":
            # Create strategy options for both computers
            self.create_strategy_option("Computer 1's Strategy:", "strategy1")
            self.create_strategy_option("Computer 2's Strategy:", "strategy2")

    def create_strategy_option(self, label_text, var_prefix):
                # Create label for strategy selection
                tk.Label(self.window, text=label_text).pack(anchor='w', padx=20, pady=10)

                # Define a StringVar for strategy option and initialize it with a value that doesn't match any radio button values
                strategy_var = tk.StringVar(value='none')
                setattr(self, var_prefix + '_strategy_var', strategy_var)

                # Define strategy options
                strategies = ["Unconditional Cooperator", "Unconditional Defector", "Random", "Tit for Tat",
                              "Probability p Cooperator"]
                for strategy in strategies:
                    radiobutton = tk.Radiobutton(
                        self.window, text=strategy, variable=strategy_var, value=strategy,
                        command=lambda s=strategy: self.on_strategy_selected(var_prefix, s)
                    )
                    radiobutton.pack(anchor='w', padx=20, pady=5)

    def on_strategy_selected(self, var_prefix, strategy):##Added function to set strategy-ANUSHKA
        attribute_name = f'{var_prefix}_selected_strategy'
        setattr(self, attribute_name, strategy)
        #print(f"Set {attribute_name} to {strategy}")  # Debugging print
        self.enable_start_button(var_prefix)

    def get_selected_strategy(self, var_prefix):
        attribute_name = f'{var_prefix}_selected_strategy'
        selected_strategy = getattr(self, attribute_name, None)
        #print(f"Retrieving {attribute_name}: {selected_strategy}")  # Debugging print
        return selected_strategy

    def enable_start_button(self, var_prefix):
        strategy_var = getattr(self, var_prefix + '_strategy_var')
        if strategy_var and strategy_var.get() != 'none':
            self.start_button['state'] = 'normal'
        else:
            self.start_button['state'] = 'disabled'

    def destroy_strategy_options(self):
        # Destroy or hide previous strategy option widgets
        for widget in self.strategy_option_widgets:
            widget.destroy()
        self.strategy_option_widgets = []  # Reset the list after destroying the widgets



    def start_experiment(self):
        # Validate the input values
        if not self.validate_inputs():
            messagebox.showerror("Invalid Input", "Please check your inputs.")
            return

        # Retrieve the selected strategies, if applicable
        #

        # Display a confirmation or start the experiment
        messagebox.showinfo("Experiment Starting", "The experiment is now starting with the provided settings.")



    def validate_inputs(self):
        # Retrieve the field values
        num_trials_str = self.num_trials_var.get()
        trial_duration_str = self.trial_duration_var.get()
        decision_time_str = self.decision_time_var.get()

        strategy1 = self.get_selected_strategy('strategy1')
        strategy2 = self.get_selected_strategy('strategy2') if self.selected_opp.get() == "computer_computer" else None
        opponent_type=self.selected_opp.get()
        if not num_trials_str or not trial_duration_str or not decision_time_str:
            messagebox.showerror("Invalid Input", "One or more fields are empty. Please fill out all fields.")
            return False

        try:
            # Convert the field values to integers
            num_trials = int(num_trials_str)
            trial_duration = int(trial_duration_str)
            decision_time = int(decision_time_str)

            # Check if the values are greater than zero
            if num_trials <= 0 or trial_duration <= 0 or decision_time <= 0:
                messagebox.showerror("Invalid Input", "Values must be greater than zero.")
                return False

            # Check if decision_time is less than or equal to trial_duration
            if decision_time > trial_duration:
                messagebox.showerror("Invalid Input", "Decision time must be less than or equal to trial duration.")
                return False

            return True

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for trials, duration, and decision time.")
            return False

    def on_start_clicked(self):


        # Retrieve settings when the button is clicked
        settings = self.get_settings()
        if settings:
            # If settings are valid, proceed with the next steps
            print("Settings retrieved:", settings)
            return settings

        else:
            # Handle the case where settings are not valid
            print("Invalid settings. Please check your inputs.")


    def get_settings(self):

        ##Anushka- validation checks
        if not self.validate_inputs():
            # If validation fails, show an error message and then close the window
            messagebox.showerror("Invalid Input",
                                 "Invalid input detected. You must restart the application to try again.")

            return None
        try:
            # Retrieve the values from StringVars
            num_trials = int(self.num_trials_var.get())
            trial_duration = int(self.trial_duration_var.get())
            decision_time = int(self.decision_time_var.get())
            opponent_type=self.selected_opp.get()

            opponent_strategy = self.get_selected_strategy('strategy1')##ANUSHKA-Changed input to be able to get opponent strategy........what about computer strategy?
            computer_opponent_strategy=self.get_selected_strategy('strategy2')
            settings = {
                'num_trials': num_trials,
                'trial_duration': trial_duration,
                'decision_time': decision_time,

                'opponent_type':opponent_type,
                'opponent_strategy': opponent_strategy,
                'computer_opponent_strategy' : computer_opponent_strategy,
            }

            #print(settings)
            return settings

        except ValueError:
            # Handle the case where the input is not a valid integer
            messagebox.showerror("Invalid Input", "Please enter valid numbers for trials, duration, and decision time.")
            return None







