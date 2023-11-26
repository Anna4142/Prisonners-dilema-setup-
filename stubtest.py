import tkinter as tk
from VideoAnalyzerStub import VideoAnalyzerStub

def main():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Video Analyzer Stub Test")

    # Create an instance of the VideoAnalyzerStub
    video_analyzer = VideoAnalyzerStub(root)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
