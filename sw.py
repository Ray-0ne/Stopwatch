import tkinter as tk
from tkinter import ttk
import time
import math


class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch with Arc Progress")
        self.root.geometry("400x500")
        self.root.configure(bg='#2c3e50')

        # Stopwatch variables
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
        self.max_time = 60  # Maximum time for full arc (60 seconds)

        # Create UI
        self.create_widgets()

        # Start the update loop
        self.update_display()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Stopwatch",
            font=("Arial", 24, "bold"),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=20)

        # Canvas for arc progress
        self.canvas = tk.Canvas(
            self.root,
            width=300,
            height=300,
            bg='#2c3e50',
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        # Time display
        self.time_label = tk.Label(
            self.root,
            text="00:00.00",
            font=("Monaco", 20, "bold"),
            fg='#3498db',
            bg='#2c3e50'
        )
        self.time_label.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=20)

        # Start/Stop button
        self.start_stop_btn = tk.Button(
            button_frame,
            text="Start",
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            bg='#27ae60',
            fg='white',
            border=0,
            command=self.toggle_stopwatch
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=10)

        # Reset button
        self.reset_btn = tk.Button(
            button_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            bg='#e74c3c',
            fg='white',
            border=0,
            command=self.reset_stopwatch
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)

        # Max time adjustment
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=10)

        tk.Label(
            control_frame,
            text="Max Time (seconds):",
            font=("Arial", 10),
            fg='white',
            bg='#2c3e50'
        ).pack(side=tk.LEFT)

        self.max_time_var = tk.StringVar(value=str(self.max_time))
        max_time_entry = tk.Entry(
            control_frame,
            textvariable=self.max_time_var,
            width=8,
            font=("Arial", 10)
        )
        max_time_entry.pack(side=tk.LEFT, padx=10)
        max_time_entry.bind('<Return>', self.update_max_time)

    def draw_arc(self):
        # Clear canvas
        self.canvas.delete("all")

        # Draw background circle
        center_x, center_y = 150, 150
        radius = 100

        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline='#34495e', width=8, fill=''
        )

        # Calculate progress
        if self.max_time > 0:
            progress = min(self.elapsed_time / self.max_time, 1.0)
        else:
            progress = 0

        # Draw progress arc
        if progress > 0:
            # Convert progress to degrees (start from top, go clockwise)
            start_angle = 90  # Start from top
            extent_angle = -360 * progress  # Negative for clockwise

            # Create gradient effect with multiple arcs
            colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71']
            segments = 20

            for i in range(int(segments * progress)):
                segment_progress = i / segments
                color_index = int(segment_progress * (len(colors) - 1))
                color = colors[min(color_index, len(colors) - 1)]

                segment_start = start_angle - (360 * segment_progress)
                segment_extent = -360 / segments

                self.canvas.create_arc(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    start=segment_start, extent=segment_extent,
                    outline=color, width=8, style='arc'
                )

        # Draw center circle with time
        self.canvas.create_oval(
            center_x - 60, center_y - 60,
            center_x + 60, center_y + 60,
            fill='#34495e', outline='#3498db', width=2
        )

        # Progress percentage text
        percentage = int(progress * 100)
        self.canvas.create_text(
            center_x, center_y - 10,
            text=f"{percentage}%",
            font=("Arial", 16, "bold"),
            fill='white'
        )

        # Status text
        status = "Running" if self.running else "Stopped"
        self.canvas.create_text(
            center_x, center_y + 15,
            text=status,
            font=("Arial", 10),
            fill='#bdc3c7'
        )

    def toggle_stopwatch(self):
        if self.running:
            self.stop_stopwatch()
        else:
            self.start_stopwatch()

    def start_stopwatch(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.start_stop_btn.config(text="Stop", bg='#e74c3c')

    def stop_stopwatch(self):
        if self.running:
            self.running = False
            self.start_stop_btn.config(text="Start", bg='#27ae60')

    def reset_stopwatch(self):
        self.running = False
        self.elapsed_time = 0
        self.start_time = 0
        self.start_stop_btn.config(text="Start", bg='#27ae60')
        self.time_label.config(text="00:00.00")
        self.draw_arc()

    def update_max_time(self, event=None):
        try:
            new_max = float(self.max_time_var.get())
            if new_max > 0:
                self.max_time = new_max
        except ValueError:
            self.max_time_var.set(str(self.max_time))

    def format_time(self, seconds):
        """Format time as MM:SS.CC"""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:05.2f}"

    def update_display(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time

        # Update time display
        formatted_time = self.format_time(self.elapsed_time)
        self.time_label.config(text=formatted_time)

        # Update arc
        self.draw_arc()

        # Schedule next update
        self.root.after(50, self.update_display)  # Update every 50ms for smooth animation


def main():
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()