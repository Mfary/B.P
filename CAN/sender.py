import can, time
from datetime import datetime, timezone
from threading import Thread

stop_flag = False

def rcv(bus):
    global stop_flag

    while True:
        if stop_flag:
            break
        data = bus.recv()
        ack_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        if data is None:
            continue
        (sender, seq, ack) = map(int, data.data.decode("ascii").split(","))
        if (sender == SENDER_ID and ack == 1):
            with open(ACK_FILE_NAME, 'a') as file:
                print(f'{seq},{ack_time:.3f}', file=file)

PERIOD = 1
SENDER_ID = 1
SENT_FILE_NAME = "data_sender.csv"
ACK_FILE_NAME = "data_sender_ack.csv"
COUNT = 1500

bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=125000)


with open(SENT_FILE_NAME, 'w') as file:
    print('sequence,send_time', file=file)
with open(ACK_FILE_NAME, 'w') as file:
    print('sequence,ack_time', file=file)

thread = Thread(target=rcv, args=(bus,))
thread.start()

try:
    for sequence in range(COUNT):
        send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()

        print(f'### Sending at {send_time:.3f}')
        bus.send(can.Message(arbitration_id=0, data=f'{SENDER_ID},{sequence},0'.encode('ascii'), is_extended_id=False))
        with open(SENT_FILE_NAME, 'a') as file:
            print(f'{sequence},{send_time:.3f}', file=file)
        time.sleep(PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
    bus.shutdown()
    stop_flag = True
    thread.join()
