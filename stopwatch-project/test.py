import tkinter as tk
import time
from tkinter import simpledialog
import datetime

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Stopwatch")
        self.root.geometry("400x500")  # Set window size
        self.root.configure(bg="#282C34")  # Dark theme background

        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
        self.laps = []
        self.countdown_time = 0
        self.is_countdown = False

        # Clock Label (Displays real-time clock)
        self.clock_label = tk.Label(root, text="", font=("Arial", 14), fg="white", bg="#282C34")
        self.clock_label.pack(pady=10)
        self.update_clock()

        # Timer Display
        self.label = tk.Label(root, text="00:00.000", font=("Arial", 40, "bold"), fg="white", bg="#282C34")
        self.label.pack(pady=10)

        # Buttons Frame
        button_frame = tk.Frame(root, bg="#282C34")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start, width=10, bg="#61AFEF", fg="white", font=("Arial", 12, "bold"))
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop, width=10, bg="#E06C75", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset, width=10, bg="#98C379", fg="white", font=("Arial", 12, "bold"))
        self.reset_button.grid(row=1, column=0, padx=5, pady=5)

        self.lap_button = tk.Button(button_frame, text="Lap", command=self.lap, width=10, bg="#C678DD", fg="white", font=("Arial", 12, "bold"))
        self.lap_button.grid(row=1, column=1, padx=5, pady=5)

        self.countdown_button = tk.Button(button_frame, text="Set Countdown", command=self.set_countdown, width=15, bg="#E5C07B", fg="black", font=("Arial", 12, "bold"))
        self.countdown_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.save_button = tk.Button(root, text="Save Times", command=self.save_to_file, width=15, bg="#D19A66", fg="white", font=("Arial", 12, "bold"))
        self.save_button.pack(pady=10)

        # Lap List
        self.lap_listbox = tk.Listbox(root, width=30, height=8, font=("Arial", 12), bg="#3E4451", fg="white")
        self.lap_listbox.pack(pady=10)

    def update(self):
        if self.running:
            current_time = time.time() - self.start_time
            total_time = self.elapsed_time + current_time

            if self.is_countdown:
                remaining_time = max(self.countdown_time - total_time, 0)
                minutes, seconds = divmod(int(remaining_time), 60)
                milliseconds = int((remaining_time % 1) * 1000)
                if remaining_time == 0:
                    self.running = False  # Stop when countdown reaches 0
            else:
                minutes, seconds = divmod(int(total_time), 60)
                milliseconds = int((total_time % 1) * 1000)

            self.label.config(text=f"{minutes:02}:{seconds:02}.{milliseconds:03}")
            self.root.after(10, self.update)

    def update_clock(self):
        """ Updates the real-time clock displayed at the top """
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_clock)

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.update()

    def stop(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False

    def reset(self):
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.laps.clear()
        self.lap_listbox.delete(0, tk.END)
        self.label.config(text="00:00.000")

    def lap(self):
        if self.running:
            total_time = self.elapsed_time + (time.time() - self.start_time)
            minutes, seconds = divmod(int(total_time), 60)
            milliseconds = int((total_time % 1) * 1000)
            lap_time = f"Lap {len(self.laps) + 1}: {minutes:02}:{seconds:02}.{milliseconds:03}"
            self.laps.append(lap_time)
            self.lap_listbox.insert(tk.END, lap_time)

    def set_countdown(self):
       self.is_countdown = True
       time_input = simpledialog.askstring("Countdown", "Enter time (MM:SS):")
       if time_input:
          try:
             minutes, seconds = map(int, time_input.split(":"))
             self.countdown_time = minutes * 60 + seconds
             self.reset()  # Reset stopwatch before countdown starts
             self.start()  # Start countdown immediately
          except ValueError:
            self.label.config(text="Invalid Format")

    def save_to_file(self):
        with open("stopwatch_times.txt", "w") as file:
            for lap in self.laps:
                file.write(lap + "\n")
        self.label.config(text="Saved to File!")

if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()
