import paho.mqtt.client as mqtt
import time, random
from string import ascii_uppercase
from datetime import datetime, timezone
from sys import getsizeof



def on_message(client, userdata, msg):
    print(msg)


MESSAGE_BROKER = "192.168.110.117"
TOPIC = "topic"
DATA_LENGTH = 1000
PUBLISH_PERIOD = 1
PREFIX_SIZE = getsizeof(bytes(f"{datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp():.3f}#", 'ascii'))
FILE_NAME = "data_sender.csv"
QOS = 0

client = mqtt.Client()
client.on_message = on_message
client.connect(MESSAGE_BROKER, 1883, 60)

with open(FILE_NAME, 'w') as file:
    print('rtt,send_time,send_time,ack_time',file=file)

try:
    client.loop_start()
    while True:
        N = DATA_LENGTH - PREFIX_SIZE
        random_string = ''.join(random.choices(ascii_uppercase, k=N))
        send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        client.publish(TOPIC, f"{send_time:.3f}#{random_string}", qos=QOS)
        ack_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        print(f'published on: {send_time:.3f}')
        with open(FILE_NAME, 'a') as file:
            print(f'{ack_time-send_time:.3f},{send_time:.3f}, {ack_time:.3f}', file=file)
        time.sleep(PUBLISH_PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
client.loop_stop()
client.disconnect()
