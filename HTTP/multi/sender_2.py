import time
from datetime import datetime, timezone
import requests



RECEIVER_IP = '192.168.105.71'
PERIOD = 1
SENDER_ID = 2
FILE_NAME = "data_sender_2.csv"
COUNT = 1500

with open(FILE_NAME, 'w') as file:
    print('sender_id,sequence,rtt,send_time,send_time,ack_time,response',file=file)

try:
    for sequence in range(COUNT):
        send_time = datetime.now(timezone.utc).timestamp()
        res = requests.post(f"http://{RECEIVER_IP}:8000", f'{SENDER_ID},{sequence},0', headers={'content-type': 'text/plain'})
        ack_time = datetime.now(timezone.utc).timestamp()
        print(f'### sent on: {send_time:.3f}')
        print(res.content.decode('ascii'))
        with open(FILE_NAME, 'a') as file:
            print(f'{SENDER_ID},{sequence},{ack_time-send_time:.3f},{send_time:.3f},{ack_time:.3f},{res.content.decode("ascii")}', file=file)
        time.sleep(PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
