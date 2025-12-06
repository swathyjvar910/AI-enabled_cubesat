# gui.app.py
import tkinter as tk
from tkinter import scrolledtext
from telemetry import append_packet, bin_file
from processing import process_telemetry
from schedular_module import start_scheduler
import os
import datetime

class TelemetryApp:
    def __init__(self, root):
        self.root = root
        root.title("AI-Enabled CubeSat Nightly Test Tool")
        root.geometry("900x500")

        title_label = tk.Label(
            root,
            text="AI-Enabled CubeSat Nightly Test Tool",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        self.log_box = scrolledtext.ScrolledText(root, width=100, height=20)
        self.log_box.pack(padx=10,pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.btn_gen1 = tk.Button(
            btn_frame,
            text="Generate 1 Telemetry Packet",
            command=self.generate_one_packet
        )
        self.btn_gen1.grid(row=0, column=0, padx=5, pady=5)

        self.btn_gen10= tk.Button(
            btn_frame,
            text="Generate 10 Telemetry Packets",
            command=self.generate_ten_packets
        )
        self.btn_gen10.grid(row=0, column=1, padx=5, pady=5)

        self.btn_proc = tk.Button(
            btn_frame,
            text="Run Processing now",
            command=self.run_processing_now
        )
        self.btn_proc.grid(row=0, column=2, padx=5, pady=5)

        self.btn_clear = tk.Button(
            btn_frame,
            text="Clear Telemetry File",
            command=self.clear_telemetry_file
        )
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5)

        self.schedule_label = tk.Label(
            root,
            text="Scheduled processing: daily at time set in scheduler_module.py",
            font=("Arial", 11)
        )
        self.schedule_label.pack(pady=5)

        self.log("Application started")
        self.log("Scheduler running in background thread")

        # Start scheduler background thread, pass GUI log as callback
        start_scheduler(self.log)

    def log(self, msg:str):
        """Log a message to the GUI text box"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {msg}"
        self.log_box.insert(tk.END, line + "\n")
        self.log_box.see(tk.END)

    def generate_one_packet(self):
        append_packet()
        self.log("Generated and saved 1 Telemetry Packet.")

    def generate_ten_packets(self):
        for i in range(10):
            append_packet()
        self.log("Generated and saved 10 Telemetry Packets.")

    def run_processing_now(self):
        msg, df = process_telemetry()
        self.log(msg)
        if df is not None and not df.empty:
            # for debugging: print last few rows in console
            print(df.tail(5))

    def clear_telemetry_file(self):
        if os.path.exists(bin_file):
            os.remove(bin_file)
            self.log("Telemetry file deleted.")
        else:
            self.log("Telemetry file not found.")

def main():
    root = tk.Tk()
    app = TelemetryApp(root)
    root.mainloop()