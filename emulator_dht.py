import sys
import random
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import paho.mqtt.client as mqtt
from mqtt_init import broker_ip, broker_port, username, password

clientname = "IOT_dht_" + str(id(object()))
topic = "parking/spot1" 

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(client_id=clientname, clean_session=True, protocol=mqtt.MQTTv311)


        self.client.username_pw_set(username, password)
        self.client.connect(broker_ip, int(broker_port))
        self.client.loop_start()

    def send_random_status(self):
        status = random.choice(["free", "occupied"])
        self.client.publish(topic, status)
        print(f"{status} sent to {topic}")

class DHTWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mqtt = MQTTClient()
        self.setWindowTitle("DHT Emulator")
        self.setGeometry(100, 100, 300, 80)

        self.label = QLabel("Sending to: " + topic)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mqtt.send_random_status)
        self.timer.start(5000)  

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
win = DHTWindow()
win.show()
sys.exit(app.exec_())
