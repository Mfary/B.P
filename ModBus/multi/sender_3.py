from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataBank
from datetime import datetime, timezone
import time, struct


HOST = "192.168.105.71"
PERIOD = 1
SENT_FILE_NAME = "data_sender_3.csv"
ACK_FILE_NAME = "data_sender_ack_3.csv"
SENDER_ID = 3
COUNT = 1500

class CustomDataBank(DataBank):
    def set_holding_registers(self, address, word_list, srv_info=None):
        ack_time = datetime.now(timezone.utc).timestamp()
        print(f'### Received at {ack_time}')
        data = struct.unpack("8s", bytes(word_list))[0].decode('ascii')
        (sender, seq, ack) = map(int, data.split(","))
        if (ack == 0):
            return
        if (sender == SENDER_ID and ack == 1):
            with open(ACK_FILE_NAME, 'a') as file:
                print(f'{sender},{seq},{ack_time:.3f}', file=file)

        return super().set_holding_registers(address, word_list, srv_info)

with open(SENT_FILE_NAME, 'w') as file:
    print('sender_id,sequence,rtt,send_time,ack_time',file=file)

with open(ACK_FILE_NAME, 'w') as file:
    print('sender_id,sequence,ack_time',file=file)

server = ModbusServer("0.0.0.0", 502, no_block=True, data_bank=CustomDataBank())
server.start()
print(f"### Server started")

try:
    for sequence in range(COUNT):
        client = ModbusClient(host=HOST, port=502, timeout=5)
        send_time = datetime.now(timezone.utc).timestamp()
        client.write_multiple_registers(0, struct.pack('8s', f'{SENDER_ID},{sequence:4d},0'.encode('ascii')))
        ack_time = datetime.now(timezone.utc).timestamp()
        print(f'### sent {sequence} on: {send_time}')
        with open(SENT_FILE_NAME, 'a') as file:
            print(f'{SENDER_ID},{sequence},{ack_time-send_time:.3f},{send_time:.3f}, {ack_time:.3f}', file=file)
        time.sleep(PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
time.sleep(5)
server.stop()
