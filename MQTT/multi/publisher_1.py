import paho.mqtt.client as mqtt
import time
from datetime import datetime, timezone



def on_message_recieve(client, userdata, msg):
    data = msg.payload.decode('ascii')
    ack_time = datetime.now(timezone.utc).timestamp()
    if data is None:
        return
    (sender, seq, ack) = map(int, data.split(","))
    if (sender == SENDER_ID and ack == 1):
        with open(ACK_FILE_NAME, 'a') as file:
            print(f'{sender},{seq},{ack_time:.3f}', file=file)


SENDER_ID = 1
MESSAGE_BROKER = "192.168.105.117"
SENDER_TOPIC = "topic"
RECEIVER_TOPIC = "res"
PUBLISH_PERIOD = 1
SENT_FILE_NAME = "data_sender_1_0.csv"
ACK_FILE_NAME = "data_sender_ack_1_0.csv"
QOS = 0
COUNT = 1500

client = mqtt.Client()
client.on_message = on_message_recieve
client.connect(MESSAGE_BROKER, 1883, 60)

with open(SENT_FILE_NAME, 'w') as file:
    print('sender_id,sequence,rtt,send_time,ack_time',file=file)

with open(ACK_FILE_NAME, 'w') as file:
    print('sender_id,sequence,ack_time',file=file)

try:
    client.loop_start()
    client.subscribe(RECEIVER_TOPIC)
    for sequence in range(COUNT):
        send_time = datetime.now(timezone.utc).timestamp()
        client.publish(SENDER_TOPIC, f'{SENDER_ID},{sequence},0'.encode('ascii'), qos=QOS)
        ack_time = datetime.now(timezone.utc).timestamp()
        print(f'published on: {send_time:.3f}')
        with open(SENT_FILE_NAME, 'a') as file:
            print(f'{SENDER_ID},{sequence},{ack_time-send_time:.3f},{send_time:.3f},{ack_time:.3f}', file=file)
        print(f'{SENDER_ID},{sequence},{ack_time-send_time:.3f},{send_time:.3f},{ack_time:.3f}')
        time.sleep(PUBLISH_PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
    time.sleep(5)
client.loop_stop()
client.disconnect()
