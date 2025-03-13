#!/usr/bin/env python

import carla
import tkinter as tk
from tkinter import messagebox
import os
import threading
import time

class CarlaRecorderGUI:
    def __init__(self, root, host, port, recorder_filename, vehicle_type):
        self.root = root
        self.root.title("Scenario Recorder")
        self.root.geometry("300x150")
        
        self.host = host
        self.port = port
        self.recorder_filename = recorder_filename
        self.vehicle_type = vehicle_type  # The vehicle type to monitor
        
        self.client = None
        self.is_recording = False
        self.filename = os.path.join(os.getcwd(), self.recorder_filename)
        self.recording_started = False  # Ensures recording starts only once when the vehicle is found

        # GUI elements
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=20)
        
        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=20)

        # Initialize the CARLA client and world
        self.client = carla.Client(self.host, self.port)
        self.client.set_timeout(2.0)
        self.world = self.client.get_world()

        # Start the thread monitoring the vehicle type spawn
        self.monitor_thread = threading.Thread(target=self.monitor_vehicle_spawn, daemon=True)
        self.monitor_thread.start()

    def start_recording(self):
        """Start recording when called from the GUI."""
        try:
            if not self.is_recording:
                print(f"Recording on file: {self.filename}")
                self.client.start_recorder(self.filename)
                self.is_recording = True
                self.recording_started = True  # Ensure it starts only once automatically
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")

    def stop_recording(self):
        """Stop recording when called from the GUI."""
        try:
            if self.client and self.is_recording:
                print("Stopping recording.")
                self.client.stop_recorder()
                self.is_recording = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording: {e}")

    def monitor_vehicle_spawn(self):
        """Monitors the world for the vehicle of type `self.vehicle_type` and starts recording when it spawns."""
        try:
            vehicle = None
            while True:
                # Get all actors (vehicles) in the world
                actors = self.world.get_actors()

                # Check if the specified vehicle type is found
                for actor in actors:
                    if actor.type_id == self.vehicle_type and not vehicle:
                        vehicle = actor
                        print(f"Vehicle of type '{self.vehicle_type}' spawned.")
                        self.start_recording()  # Start recording when the vehicle spawns
                        break  # Stop checking further once the vehicle is found

                # If vehicle is found, stop monitoring and continue recording
                if vehicle:
                    print(f"Vehicle spawned, monitoring stopped.")
                    break  # Stop the thread once the vehicle has been found

       
        
        except Exception as e:
            print(f"Error monitoring vehicle spawn: {e}")

    def exit_program(self):
        """Stops the recording and exits the program."""
        if self.is_recording:
            self.client.stop_recorder()
        self.root.quit()

def main():
    host = "127.0.0.1"
    port = 2000
    recorder_filename = "test.log"
    vehicle_type = "vehicle.lincoln.mkz_2017"  # The vehicle type to monitor
    
    # Create the Tkinter root window
    root = tk.Tk()
    app = CarlaRecorderGUI(root, host, port, recorder_filename, vehicle_type)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == '__main__':
    main()

