import socket

nb = 1  # 0 = broker של המכללה, 1 = broker ציבורי (HiveMQ)

brokers = [
    str(socket.gethostbyname('vmm1.saaintertrade.com')),
    str(socket.gethostbyname('broker.hivemq.com'))
]

ports = ['80', '1883']
usernames = ['MATZI', '']
passwords = ['MATZI', '']

pub_topic = "IOT/class/house/sensor/1/2524"
sub_topic = "IOT/class/house/sensor/1/2524"

broker_ip = brokers[nb]
broker_port = int(ports[nb])
username = usernames[nb]
password = passwords[nb]