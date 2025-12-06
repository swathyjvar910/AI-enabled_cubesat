# schedular_module.py
import datetime
import time
import threading
from processing import process_telemetry

# default schedule time (24-hr format)
schedule_hour = 2 # 2 am
schedule_minute = 0 # 02:00

def scheduler_loop(callback):
    """Background loop that checks the time and runs processing at the scheduled hour and minute.
       callback(msg: str) is used to send status messages back (GUI will pass its log function)."""
    last_run_minute = None
    while True:
        now = datetime.datetime.now()
        current_minute_key = now.strftime("%Y-%m-%d %H:%M")

        if (
            now.hour == schedule_hour
            and now.minute == schedule_minute
            and current_minute_key != last_run_minute
        ):
            last_run_minute = current_minute_key
            callback("Running scheduled nightly processing...")
            msg, df = process_telemetry()
            callback("[Scheduled]" + msg)
            # Sleep more than a minute to avoid duplicate runs
            time.sleep(70)
        time.sleep(5)

def start_scheduler(callback):
    """Starts the scheduler in a background daemon thread."""
    t = threading.Thread(target=scheduler_loop, args=(callback,), daemon=True)
    t.start()
