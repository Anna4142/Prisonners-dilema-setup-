import pygame

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        # Dictionary to hold sounds
        self.sounds = {}

    def load_sound(self, sound_name, file_path):
        """Load a sound from a file and store it in the dictionary."""
        self.sounds[sound_name] = pygame.mixer.Sound(file_path)

    def play_sound(self, sound_name):
        """Play a sound by its name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found")

    def stop_sound(self, sound_name):
        """Stop a sound by its name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
        else:
            print(f"Sound '{sound_name}' not found")
