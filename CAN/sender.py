import can, time, os, struct
from datetime import datetime, timezone

FILE_NAME = "data_sender.csv"
PERIOD = 1

bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=125000)

with open(FILE_NAME, 'w') as file:
    print('rtt,send_time,send_time,ack_time',file=file)

try:
    while True:
        send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        data = struct.pack('d', send_time)
        print(f"### Sending at {send_time:.3f}")
        bus.send(can.Message(arbitration_id=0, data=data, is_extended_id=False))
        ack_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        with open(FILE_NAME, 'a') as file:
            print(f'{ack_time-send_time:.3f},{send_time:.3f}, {ack_time:.3f}', file=file)
        time.sleep(PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
    bus.shutdown()
