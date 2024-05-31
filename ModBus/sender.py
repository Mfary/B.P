from pyModbusTCP.client import ModbusClient
from datetime import datetime, timezone
import time, struct


HOST = "192.168.110.71"
PERIOD = 1
FILE_NAME = "data_sender.csv"

with open(FILE_NAME, 'w') as file:
    print('rtt,send_time,send_time,ack_time',file=file)

try:
    while True:
        client = ModbusClient(host=HOST, port=502, timeout=5)
        send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        client.write_multiple_registers(0, struct.pack('d', send_time))
        ack_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        print(f'### sent on: {send_time}')
        with open(FILE_NAME, 'a') as file:
            print(f'{ack_time-send_time:.3f},{send_time:.3f}, {ack_time:.3f}', file=file)
        time.sleep(PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
