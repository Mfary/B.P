import paho.mqtt.client as mqtt
from datetime import datetime, timezone

def on_message(client, userdata, msg):
    data = msg.payload.decode('ascii')
    receive_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    if data is None:
        return
    (sender, seq, ack) = map(int, data.split(","))
    if (ack == 1):
        return

    client.publish(RECEIVER_TOPIC, f'{sender},{seq},1'.encode('ascii'), qos=QOS)

    print(f"### Received at {receive_time:.3f}")

    with open(FILE_NAME, 'a') as file:
        print(f'{sender},{seq},{receive_time:.3f}', file=file)


MESSAGE_BROKER = "192.168.105.117"
SENDER_TOPIC = "topic"
RECEIVER_TOPIC = "res"
FILE_NAME = "data_receive_0.csv"
QOS = 0

client = mqtt.Client()
client.on_message = on_message
client.connect(MESSAGE_BROKER, 1883, 60)

with open(FILE_NAME, 'w') as file:
    print('sender_id,sequence,receive_time',file=file)

try:
    client.loop_start()
    client.subscribe(SENDER_TOPIC)
    while True:
        pass
except KeyboardInterrupt:
    print('### Stopping gracefully...')
client.loop_stop()
client.disconnect()
