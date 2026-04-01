import psutil
import json
import os
from pynput import keyboard
from datetime import datetime
import threading

# Initialize or load existing alerts
ALERTS_FILE = "alerts.json"

def save_alert(threat_message):
    alert_data = []
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as file:
            try:
                alert_data = json.load(file)
            except json.JSONDecodeError:
                alert_data = []

    new_alert = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "threat": threat_message,
        "status": "Critical"
    }
    alert_data.insert(0, new_alert) # Put newest alerts at the top
    
    with open(ALERTS_FILE, "w") as file:
        json.dump(alert_data[:20], file, indent=4) # Keep last 20 alerts

def scan_processes():
    suspicious_names = ["keylogger", "logger", "spy", "monitor", "hook"]
    for process in psutil.process_iter(['name']):
        try:
            name = process.info['name'].lower()
            if any(word in name for word in suspicious_names):
                save_alert(f"Suspicious Process Found: {name}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

# Monitoring logic
key_count = 0
def on_press(key):
    global key_count
    key_count += 1
    if key_count >= 100: # Threshold for unusual rapid typing
        save_alert("High-frequency keyboard activity detected (Potential Hook)")
        key_count = 0

def start_monitoring():
    scan_processes()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    print("🛡️ Monitoring System Active...")
    start_monitoring()