#!/usr/bin/env python

import carla
import tkinter as tk
from tkinter import messagebox
import os
import json
import threading
import math
import time



class CarlaRecorderGUI:
    def __init__(self, root, host, port, recorder_filename):
        self.root = root
        self.root.title("Scenario Recorder")
        self.root.geometry("300x150")
        
        self.host = host
        self.port = port
        self.recorder_filename = recorder_filename
        
        self.client = None
        self.is_recording = False
        self.filename = os.path.join(os.getcwd(), self.recorder_filename)

        # GUI elements
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=20)
        
        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=20)


    def start_recording(self):
        try:
            if self.client is None:
                self.client = carla.Client(self.host, self.port)
                self.client.set_timeout(2.0)

            print("Recording on file: %s" % self.filename)
            self.client.start_recorder(self.filename)
            self.is_recording = True

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)


        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")

    def stop_recording(self):
        try:
            if self.client and self.is_recording:
                print("Stopping recording.")
                self.client.stop_recorder()
                self.is_recording = False

                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording: {e}")

   
    def exit_program(self):
        if self.is_recording:
            self.client.stop_recorder()
        self.root.quit()


def main():
    # Command-line arguments (if you want to modify these)
    host = "127.0.0.1"
    port = 2000
    recorder_filename = "test.log"

    root = tk.Tk()
    app = CarlaRecorderGUI(root, host, port, recorder_filename)
    
    # Run the GUI
    root.mainloop()


if __name__ == '__main__':
    main()


