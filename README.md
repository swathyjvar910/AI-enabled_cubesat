AI-Enabled CubeSat Nightly Test Tool
A Python-based tool that simulates CubeSat telemetry, stores it in binary format, processes it automatically at a scheduled time, and uses AI to detect anomalies — all through an interactive GUI.

🚀 Project Overview

CubeSats generate health telemetry continuously. Monitoring this data manually is inefficient and error-prone.
This project provides an automated system that:
Generates sample CubeSat telemetry packets
Saves them in a binary .bin file
Performs nightly scheduled data processing
Uses AI (IsolationForest) for anomaly detection
Provides an interactive Tkinter GUI for users
This project is fully implemented in Python and runs on a normal laptop.

cubesat_ai_project/
│
├── telemetry.py          # Telemetry packet generation & binary file handling
├── processing.py         # Data processing + AI anomaly detection 
├── scheduler_module.py   # Nightly scheduler using background thread
├── gui_app.py            # Tkinter-based GUI
├── main.py               # Entry point to start the application
│
└── telemetry.bin         # Generated binary telemetry data (auto created)
