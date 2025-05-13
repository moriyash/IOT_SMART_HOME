import subprocess
import time
import sys
from PyQt5.QtWidgets import QApplication
from monitor_gui import StartWindow

emulators = [
    "emulator_dht.py",
    "emulator_button.py",
    "emulator_relay.py"
]

processes = []
for emulator in emulators:
    p = subprocess.Popen([sys.executable, emulator])
    processes.append(p)
    time.sleep(0.5)  

app = QApplication(sys.argv)
window = StartWindow()
window.show()
exit_code = app.exec_()

for p in processes:
    p.terminate()
