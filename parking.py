import os
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
from mqtt_init import broker_ip, broker_port, username, password

# MQTT הגדרות
sub_topic_base = "parking/spot"

# יצירת Client ID ייחודי
r = random.randrange(1, 100000)
clientname = "IOT_client-325012524-" + str(r)

# מחלקת MQTT
class Mqtt_client():
    def __init__(self):
        self.broker = broker_ip
        self.port = int(broker_port)
        self.clientname = clientname
        self.username = username
        self.password = password
        self.client = mqtt.Client(self.clientname, clean_session=True)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)

    def start(self):
        self.client.loop_start()
        for i in range(10):
            self.client.subscribe(f"{sub_topic_base}{i+1}")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to broker")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        index = int(topic.replace(sub_topic_base, "")) - 1
        mainwin.parkingDock.update_spot_status(index, payload)

    def publish_to(self, topic, message):
        self.client.publish(topic, message)

# מחלקת GUI לחניות
class ParkingDock(QDockWidget):
    def __init__(self, mc):
        super().__init__()
        self.mc = mc
        self.buttons = []
        self.status = {}
        self.grid = QGridLayout()

        for i in range(10):
            btn = QPushButton(f"Spot {i + 1}")
            btn.setFixedSize(100, 50)
            btn.setStyleSheet("background-color: lightgray")
            btn.clicked.connect(lambda checked, index=i: self.reserve_spot(index))
            self.grid.addWidget(btn, i // 5, i % 5)
            self.buttons.append(btn)
            self.status[i] = "free"

        container = QWidget()
        container.setLayout(self.grid)
        self.setWidget(container)
        self.setWindowTitle("Parking Spots")

    def reserve_spot(self, index):
        if self.status[index] == "free":
            topic = f"{sub_topic_base}{index + 1}/command"
            self.mc.publish_to(topic, "reserve")
            print(f"Requested reservation for Spot {index + 1}")

    def update_spot_status(self, index, state):
        self.status[index] = state
        color = {
            "free": "lightgreen",
            "occupied": "red",
            "reserved": "lightblue"
        }.get(state, "gray")
        self.buttons[index].setStyleSheet(f"background-color: {color}")

# חלון ראשי
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("Smart Parking Monitor")
        self.mc = Mqtt_client()
        self.parkingDock = ParkingDock(self.mc)
        self.addDockWidget(Qt.TopDockWidgetArea, self.parkingDock)
        self.mc.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec_())
