import time, random
from string import ascii_uppercase
from datetime import datetime, timezone
from sys import getsizeof
import requests



RECEIVER_IP = '192.168.110.71'
DATA_LENGTH = 1000
PERIOD = 10
PREFIX_SIZE = getsizeof(bytes(f"{datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp():.3f}#", 'ascii'))
FILE_NAME = "data_sender.csv"

with open(FILE_NAME, 'w') as file:
    print('rtt,send_time,send_time,ack_time',file=file)

while True:
    N = DATA_LENGTH - PREFIX_SIZE
    random_string = ''.join(random.choices(ascii_uppercase, k=N))
    send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    requests.post(f"http://{RECEIVER_IP}:8000", f'{send_time:.3f}#{random_string}', headers={'content-type': 'text/plain'})
    ack_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    print(f'### sent on: {send_time}')
    with open(FILE_NAME, 'a') as file:
        print(f'{ack_time-send_time:.3f},{send_time:.3f}, {ack_time:.3f}', file=file)
    time.sleep(PERIOD)
