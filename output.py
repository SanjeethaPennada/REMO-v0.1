import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import json
from PIL import Image, ImageTk, ImageSequence
import os

class BlockDiagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("REMO - Record, Replay with Modifications")
        
        # Set the size of the window
        self.root.geometry("600x600")
        
        # Load GIFs for display
        self.failure_scenario_gif = 'original_scenario.gif'  # Original scenario GIF
        self.modified_scenario_gif = 'modified_scenario.gif'  # Modified scenario GIF
        
        # Set up the GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Create Title for the GUI
        title_label = tk.Label(self.root, text="(REMO) Replay With Modifications", font=("Arial", 30))
        title_label.grid(row=0, column=4, pady=20)

        # Create a Canvas for drawing arrows
        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.grid(row=2, column=4, columnspan=6)

        # Block for Failure Scenario
        self.failure_scenario_label = tk.Label(self.root, text="Failure Scenario + Transfuser ADS", font=("Arial", 18))
        self.failure_scenario_label.grid(row=1, column=3, pady=20, padx=20)
        
        self.failure_scenario_display = self.create_gif_display(self.failure_scenario_gif)
        self.failure_scenario_display.grid(row=2, column=3)

        # Block for REMO
        remo_label = tk.Label(self.root, text="REMO", font=("Arial", 25), width=15, height=6, relief="solid")
        remo_label.grid(row=2, column=5, padx=25, pady=25)


        # Modified Scenario Block
        modified_scenario_label = tk.Label(self.root, text="Modified Scenario", font=("Arial", 18))
        modified_scenario_label.grid(row=1, column=7, padx=20, pady=20)
       
        self.modified_scenario_display = self.create_gif_display(self.modified_scenario_gif)  # Initially shows modified scenario
        self.modified_scenario_display.grid(row=2, column=7)

        # Draw arrows using the canvas
        self.add_arrows()

    def create_gif_display(self, gif_path):
        """Create a label widget that displays a GIF and animates it."""
        gif_label = tk.Label(self.root)
        gif_frames = self.load_gif(gif_path)  # Load the GIF frames specific to this scenario
        current_frame = 0
        
        # Set the first frame for the initial display
        gif_label.configure(image=gif_frames[current_frame])
        
        # Start animating the gif
        self.animate_gif(gif_label, gif_frames, current_frame)
        
        return gif_label

    def load_gif(self, gif_path):
        """Load the GIF and return the frames."""
        gif = Image.open(gif_path)
        frames = []
        
        # Loop through all frames in the GIF and convert them into ImageTk.PhotoImage
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")  # Ensure it's RGBA to match Tkinter compatibility
            frame = frame.resize((500,500))  # Resize the frame if necessary
            frames.append(ImageTk.PhotoImage(frame))
        
        return frames

    def animate_gif(self, gif_label, gif_frames, current_frame):
        """Animate the GIF by cycling through its frames."""
        current_frame += 1
        if current_frame >= len(gif_frames):
            current_frame = 0  # Loop back to the first frame
        
        # Update the image on the label with the current frame
        gif_label.configure(image=gif_frames[current_frame])
        
        # Schedule the next frame update (animation)
        self.root.after(100, self.animate_gif, gif_label, gif_frames, current_frame)

    def load_location_json(self):
        """Open the location.json or output.json file and apply modifications."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    location_data = json.load(f)
                print(f"Loaded modifications from {file_path}")
                self.apply_modifications(location_data)
            except Exception as e:
                print(f"Error loading JSON: {e}")
                messagebox.showerror("Error", f"Failed to load {file_path}. Please check the file format.")

    def apply_modifications(self, location_data):
        """Apply modifications (This is a placeholder for applying the loaded modifications)."""
        print("Applying modifications...")
        
        # Here, you can handle the logic to update or change the scenario based on the JSON file
        # For now, we simulate this by switching to the modified scenario GIF
        self.modified_scenario_display.configure(image=self.modified_scenario_display.cget("image"))

        # Simulate playing the modified scenario (show first frame for now)
        print("Modifications applied. Playing Modified Scenario...")


    def add_arrows(self):
        """Add arrows between the blocks to represent the flow in the block diagram."""
        arrow_1 = tk.Label(self.root, text="--->", font=("Arial", 14))
        arrow_1.grid(row=2, column=4, padx=20)
        
        arrow_2 = tk.Label(self.root, text="--->", font=("Arial", 14))
        arrow_2.grid(row=2, column=6, padx=20)

        
# Initialize the main window
root = tk.Tk()

# Create the application
app = BlockDiagramApp(root)

# Run the Tkinter main loop
root.mainloop()


