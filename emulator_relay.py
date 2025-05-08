import sys
import time
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import paho.mqtt.client as mqtt
from mqtt_init import broker_ip, broker_port, username, password

clientname = "IOT_relay_" + str(id(object()))
topic = "parking/spot1"

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(clientname, clean_session=True)
        self.client.username_pw_set(username, password)
        self.client.connect(broker_ip, int(broker_port))
        self.client.loop_start()

    def release_spot(self):
        self.client.publish(topic, "free")
        print(f"free sent to {topic}")

class RelayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mqtt = MQTTClient()
        self.setWindowTitle("Relay Emulator")
        self.setGeometry(100, 100, 300, 100)

        self.releaseButton = QPushButton("Release Spot", self)
        self.releaseButton.setStyleSheet("background-color: orange")
        self.releaseButton.clicked.connect(self.release_now)

        layout = QVBoxLayout()
        layout.addWidget(self.releaseButton)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def release_now(self):
        self.mqtt.release_spot()
        self.releaseButton.setStyleSheet("background-color: green")

app = QApplication(sys.argv)
win = RelayWindow()
win.show()
sys.exit(app.exec_())
