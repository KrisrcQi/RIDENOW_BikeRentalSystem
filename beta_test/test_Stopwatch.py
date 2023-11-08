import tkinter as tk
from datetime import timedelta
import time

class StopwatchApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Stopwatch")

        self.start_time = None
        self.stop_time = None
        self.running = False

        self.label_var = tk.StringVar()
        self.label_var.set("00:00:00.000")

        self.label = tk.Label(root, textvariable=self.label_var, font=("Helvetica", 24))
        self.label.pack(padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_stop)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(pady=5)

        self.riding_time_var = tk.StringVar()

        self.update()

    def start_stop(self):
        if self.running:
            self.stop_time = self.elapsed_time()
            self.running = False
            self.riding_time_var.set(self.format_time(self.stop_time))
        else:
            self.start()

    def start(self):
        self.running = True
        self.start_time = time.time()

    def reset(self):
        if not self.running:
            self.start()
        else:
            self.stop_time = self.elapsed_time()
            self.running = False
            self.riding_time_var.set(self.format_time(self.stop_time))
        riding_time = self.riding_time_var.get()
        print("Running Time:", self.riding_time_var.get())
        self.riding_time_var.set("")
        return riding_time

    def elapsed_time(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def format_time(self, seconds):
        return str(timedelta(seconds=seconds))[:-4]  # Remove milliseconds

    def update(self):
        if self.running:
            elapsed_time = self.elapsed_time()
            formatted_time = self.format_time(elapsed_time)
            self.label_var.set(formatted_time)
        else:
            if self.stop_time is not None:
                formatted_time = self.format_time(self.stop_time)
                self.label_var.set(formatted_time)
            else:
                self.label_var.set("00:00:00.000")

        self.root.after(10, self.update)  # Update every 10 milliseconds


if __name__ == "__main__":

    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()


