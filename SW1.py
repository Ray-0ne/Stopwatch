import tkinter as tk
from tkinter import ttk, messagebox
import time
import pygame
import os
import urllib.request


class StopwatchApp:
    def __init__(self, root):
        pygame.mixer.init()
        self.root = root
        self.root.title("Countdown Stopwatch")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Try to set a modern theme if available
        try:
            self.root.tk.call("source", "azure.tcl")
            self.root.tk.call("set_theme", "dark")
        except:
            pass

        self.running = False
        self.remaining_time = 0
        self.start_time = 0
        self.total_time = 0

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TButton", font=("Helvetica", 10), padding=5)
        self.style.configure("TLabel", font=("Helvetica", 12), background="#2c3e50", foreground="white")
        self.style.configure("TEntry", font=("Helvetica", 12))

        self.create_widgets()
        self.download_sound()

    def download_sound(self):
        sound_url = "https://assets.mixkit.co/sfx/preview/mixkit-positive-interface-beep-221.mp3"
        sound_path = "notification.mp3"

        if not os.path.exists(sound_path):
            try:
                urllib.request.urlretrieve(sound_url, sound_path)
            except Exception as e:
                print(f"Error downloading sound: {e}")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Time Input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=20, fill=tk.X)

        ttk.Label(input_frame, text="Set Time (HH:MM:SS):").pack(side=tk.LEFT, padx=5)

        self.time_entry = ttk.Entry(input_frame, width=10)
        self.time_entry.insert(0, "00:05:00")  # Default 5 minutes
        self.time_entry.pack(side=tk.LEFT, padx=5)

        # Time Display
        time_frame = ttk.Frame(main_frame)
        time_frame.pack(pady=30)

        self.time_display = ttk.Label(time_frame, text="00:00:00", font=("Helvetica", 32))
        self.time_display.pack()

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def parse_time(self, time_str):
        try:
            hours, minutes, seconds = map(int, time_str.split(':'))
            return hours * 3600 + minutes * 60 + seconds
        except:
            return 0

    def time_to_str(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        if self.running:
            current_time = time.time()
            elapsed = current_time - self.start_time
            remaining = max(0, self.total_time - elapsed)
            self.remaining_time = remaining

            # Update time display
            self.time_display.config(text=self.time_to_str(int(remaining)))

            if remaining <= 0:
                self.stop_timer()
                self.play_notification()
            else:
                self.root.after(200, self.update_timer)

    def play_notification(self):
        sound_path = "notification.mp3"
        if os.path.exists(sound_path):
            try:
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
            except:
                pass
        messagebox.showinfo("Time's Up!", "The countdown has completed!")

    def start_timer(self):
        if not self.running:
            time_str = self.time_entry.get()
            total_seconds = self.parse_time(time_str)

            if total_seconds <= 0:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM:SS")
                return

            self.total_time = total_seconds
            self.remaining_time = total_seconds
            self.start_time = time.time()
            self.running = True
            self.start_button.config(text="Pause", command=self.pause_timer)
            self.update_timer()

    def pause_timer(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Resume", command=self.resume_timer)

    def resume_timer(self):
        if not self.running:
            self.total_time = self.remaining_time
            self.start_time = time.time() - (self.total_time - self.remaining_time)
            self.running = True
            self.start_button.config(text="Pause", command=self.pause_timer)
            self.update_timer()

    def stop_timer(self):
        self.running = False
        self.start_button.config(text="Start", command=self.start_timer)

    def reset_timer(self):
        self.stop_timer()
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "00:05:00")
        self.time_display.config(text="00:00:00")


if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
