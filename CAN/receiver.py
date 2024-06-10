import can
from datetime import datetime, timezone

FILE_NAME = "data_receiver.csv"

def rcv(bus):
    while True:
        data = bus.recv()
        receive_time = datetime.now(timezone.utc).timestamp()
        if data is None:
            continue
        (sender, seq, ack) = map(int, data.data.decode("ascii").split(","))
        if (ack == 1):
            continue

        bus.send(can.Message(arbitration_id=0, data=f'{sender},{seq},1'.encode('ascii'), is_extended_id=False))

        print(f"### Received at {receive_time:.3f}")

        with open(FILE_NAME, 'a') as file:
            print(f'{sender},{seq},{receive_time:.3f}', file=file)

with open(FILE_NAME, 'w') as file:
    print('sender_id,sequence,receive_time', file=file)

bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=125000)

try:
    rcv(bus)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
    bus.shutdown()

