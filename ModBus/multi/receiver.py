from pyModbusTCP.server import ModbusServer, DataBank
from pyModbusTCP.client import ModbusClient
from datetime import datetime, timezone
import struct


FILE_NAME = "data_recieiver.csv"
SENDER_ADDRESS = {
    1: "192.168.105.183",
    2: "192.168.105.183",
    3: "192.168.105.183",
    4: "192.168.105.",
    5: "192.168.105.",
    6: "192.168.105.",
}


class CustomDataBank(DataBank):
    def set_holding_registers(self, address, word_list, srv_info=None):
        receive_time = datetime.now(timezone.utc).timestamp()
        print(f'### Received at {receive_time}')
        print(address)
        data = struct.unpack("8s", bytes(word_list))[0].decode('ascii')
        print(data)
        (sender, seq, ack) = map(int, data.split(","))
        if (ack == 1):
            return


        client = ModbusClient(host=SENDER_ADDRESS[sender], port=502, timeout=5)
        client.write_multiple_registers(0, struct.pack('8s', f'{sender},{seq:4d},1'.encode('ascii')))
        with open(FILE_NAME, 'a') as file:
            print(f'{sender},{seq},{receive_time:.3f}', file=file)

        return super().set_holding_registers(address, word_list, srv_info)

with open(FILE_NAME, 'w') as file:
    print('sender_id,sequence,receive_time', file=file)

server = ModbusServer("0.0.0.0", 502, no_block=True, data_bank=CustomDataBank())
server.start()
print(f"### Server started")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("### Stopping gracefully...")

server.stop()
