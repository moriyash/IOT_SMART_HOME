# run_all.py
import subprocess
import time
import sys
from PyQt5.QtWidgets import QApplication
from monitor_gui import StartWindow

# Step 1: Launch emulators as separate processes
emulators = [
    "emulator_dht.py",
    "emulator_button.py",
    "emulator_relay.py"
]

processes = []
for emulator in emulators:
    p = subprocess.Popen([sys.executable, emulator])
    processes.append(p)
    time.sleep(0.5)  # slight delay between launches

# Step 2: Launch GUI
app = QApplication(sys.argv)
window = StartWindow()
window.show()
exit_code = app.exec_()

# Step 3: Terminate all emulator processes after GUI closes
for p in processes:
    p.terminate()
