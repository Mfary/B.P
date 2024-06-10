from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from datetime import datetime, timezone


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        with open('server.log', 'a') as f:
            f.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def respond(self, status=200, msg='ok'):
        self.send_response(status)
        self.end_headers()
        self.wfile.write(bytes(msg.encode()))

    def do_POST(self):
        receive_time = datetime.now(timezone.utc).timestamp()
        content_length = int(self.headers.get('content-length', 0))


        msg = self.rfile.read(content_length).decode('ascii')
        (sender, seq, ack) = map(int, msg.split(","))
        if (ack == 1):
            return
        print(msg)
        print(f'### Received at {receive_time:.3f}')

        with open(FILE_NAME, 'a') as file:
            print(f'{sender},{seq},{receive_time:.3f}',file=file)

        self.respond(msg=f'{sender},{seq},1')

    def do_GET(self):
        self.respond(HTTPStatus.METHOD_NOT_ALLOWED, 'method not allowed!')

FILE_NAME = "data_receiver.csv"

with open(FILE_NAME, 'w') as file:
    print('sender_id,sequence,receive_time',file=file)

try:
    my_server = HTTPServer(("0.0.0.0", 8000), Handler)
    print(f"### Server started")
    my_server.serve_forever()
except KeyboardInterrupt:
    print("### Stopping gracefully...")

my_server.shutdown()
