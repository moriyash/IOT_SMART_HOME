import time
import random
import paho.mqtt.client as mqtt
from mqtt_init import broker_ip, broker_port, username, password

client = mqtt.Client("Emulator-DHT", clean_session=True)
client.username_pw_set(username, password)
client.connect(broker_ip, int(broker_port))
client.loop_start()

# סימולציה לחיישן חניה: occupied / free
spot_count = 10

try:
    while True:
        spot = random.randint(1, spot_count)
        status = random.choice(["occupied", "free"])
        topic = f"parking/spot{spot}"
        print(f"Sending {status} to {topic}")
        client.publish(topic, status)
        time.sleep(random.uniform(2, 5))

except KeyboardInterrupt:
    print("Emulator stopped.")
    client.loop_stop()
    client.disconnect()
