import sys
from PyQt5.QtWidgets import *
import paho.mqtt.client as mqtt
from mqtt_init import broker_ip, broker_port, username, password

clientname = "IOT_button_" + str(id(object()))

class MQTTClient:
    def __init__(self, topic):
        self.topic = topic
        self.client = mqtt.Client(client_id=clientname, clean_session=True, protocol=mqtt.MQTTv311)
        self.client.username_pw_set(username, password)
        self.client.connect(broker_ip, int(broker_port))
        self.client.loop_start()

    def send_reserved(self):
        self.client.publish(self.topic, "reserved")
        print(f"reserved sent to {self.topic}")

class ButtonWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        spot_number, ok = QInputDialog.getInt(self, "Choose Spot", "Enter spot number (1–10):", 1, 1, 10)
        self.topic = f"parking/spot{spot_number}"
        self.mqtt = MQTTClient(self.topic)

        self.setWindowTitle(f"Button - Spot {spot_number}")
        self.setGeometry(100, 100, 300, 80)

        self.button = QPushButton(f"Reserve Spot {spot_number}", self)
        self.button.clicked.connect(self.on_click)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def on_click(self):
        self.mqtt.send_reserved()
        self.button.setStyleSheet("background-color: green")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ButtonWindow()
    win.show()
    sys.exit(app.exec_())
