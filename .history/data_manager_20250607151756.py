import paho.mqtt.client as mqtt
import sqlite3
import time
from datetime import datetime
from mqtt_init import broker_ip, broker_port, username, password

DB_FILE = 'parking_data.db'
clientname = "IOT_data_manager"
sub_topic_base = "parking/spot"
pub_alarm_topic = "parking/alarm"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    print("DB path:", os.path.abspath(DB_FILE))  # 👈 כאן נכניס את זה
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS parking_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    spot TEXT,
                    status TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()


def save_to_db(spot, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO parking_log (spot, status, timestamp) VALUES (?, ?, ?)",
              (spot, status, datetime.now().isoformat(timespec='seconds')))
    conn.commit()
    conn.close()

def check_for_alarms(client):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT spot, MAX(timestamp) FROM parking_log WHERE status='occupied' GROUP BY spot")
    rows = c.fetchall()
    now = datetime.now()
    for spot, last_time in rows:
        last_dt = datetime.fromisoformat(last_time)
        if (now - last_dt).seconds > 1800:  # 30 דקות
            msg = f"ALARM: {spot} occupied too long"
            client.publish(pub_alarm_topic, msg)
            print(msg)
    conn.close()

def on_message(client, userdata, msg):
    topic = msg.topic
    status = msg.payload.decode("utf-8")
    if topic.startswith(sub_topic_base):
        spot = topic.replace(sub_topic_base, "spot ")
        print(f"{spot} → {status}")
        save_to_db(spot, status)
        check_for_alarms(client)

def main():
    init_db()
    client = mqtt.Client(client_id="data_manage24", clean_session=True, protocol=mqtt.MQTTv311)

    client.username_pw_set(username, password)
    client.on_message = on_message
    client.connect(broker_ip, int(broker_port))
    client.loop_start()

    for i in range(1, 11):
        client.subscribe(f"{sub_topic_base}{i}")
        print(f"Subscribed to {sub_topic_base}{i}")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Data manager stopped.")
        client.loop_stop()

if __name__ == "__main__":
    main()
