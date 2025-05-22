import sys
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mqtt_init import broker_ip, broker_port, username, password

clientname = "IOT_monitor_gui"
sub_topic_base = "parking/spot"
alarm_topic = "parking/alarm"

class MQTTClient:
    def __init__(self, gui):
        self.gui = gui
        self.client = mqtt.Client(client_id=clientname, clean_session=True, protocol=mqtt.MQTTv311)
        self.client.username_pw_set(username, password)
        self.client.on_message = self.on_message
        self.client.connect(broker_ip, int(broker_port))
        self.client.loop_start()
        for i in range(1, 11):
            self.client.subscribe(f"{sub_topic_base}{i}")
        self.client.subscribe(alarm_topic)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        message = msg.payload.decode("utf-8")
        if topic.startswith(sub_topic_base):
            index = int(topic.replace(sub_topic_base, "")) - 1
            self.gui.update_spot(index, message)
        elif topic == alarm_topic:
            self.gui.append_alarm(message)

    def publish_reservation(self, spot):
        self.client.publish(f"{sub_topic_base}{spot}", "reserved")

    def publish_cancel(self, spot):
        self.client.publish(f"{sub_topic_base}{spot}", "free")

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Parking App")
        self.setGeometry(200, 200, 300, 150)

        self.label = QLabel("Welcome to Smart Parking", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Enter", self)
        self.start_button.clicked.connect(self.enter_app)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def enter_app(self):
        self.main_window = MonitorGUI()
        self.main_window.show()
        self.close()

class MonitorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Monitor")
        self.setGeometry(100, 100, 600, 400)

        self.status_buttons = []
        self.reserve_buttons = []
        self.cancel_buttons = []
        self.alarm_box = QTextEdit()
        self.alarm_box.setReadOnly(True)

        grid = QGridLayout()
        for i in range(10):
            btn = QPushButton(f"Spot {i+1}")
            btn.setEnabled(False)
            btn.setStyleSheet("background-color: lightgray")
            self.status_buttons.append(btn)

            res_btn = QPushButton("Reserve")
            res_btn.clicked.connect(lambda checked, x=i: self.reserve_spot(x))
            self.reserve_buttons.append(res_btn)

            cancel_btn = QPushButton("Cancel")
            cancel_btn.clicked.connect(lambda checked, x=i: self.cancel_spot(x))
            self.cancel_buttons.append(cancel_btn)

            grid.addWidget(btn, i, 0)
            grid.addWidget(res_btn, i, 1)
            grid.addWidget(cancel_btn, i, 2)

        layout = QVBoxLayout()
        layout.addLayout(grid)
        self.status_label = QLabel("System status will appear here")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: blue;")
        layout.addWidget(self.status_label)

        layout.addWidget(QLabel("Alarms:"))
        layout.addWidget(self.alarm_box)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.mqtt = MQTTClient(self)

    def update_spot(self, index, status):
        colors = {
            "free": "lightgreen",
            "occupied": "red",
            "reserved": "lightblue"
        }
        self.status_buttons[index].setStyleSheet(f"background-color: {colors.get(status, 'gray')}")
        self.update_status_label()


    def append_alarm(self, msg):
        self.alarm_box.append(msg)

    def reserve_spot(self, index):
        self.mqtt.publish_reservation(index + 1)

    def cancel_spot(self, index):
        self.mqtt.publish_cancel(index + 1)

    def update_status_label(self):
     colors = [btn.palette().button().color().name() for btn in self.status_buttons]
     if all(c == "#ff0000" for c in colors):
        self.status_label.setText("All parking spots are occupied")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
     else:
        self.status_label.setText("Parking spots available")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = StartWindow()
    start.show()
    sys.exit(app.exec_())
