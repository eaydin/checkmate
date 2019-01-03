import json
import threading
import datetime
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


class MateRequestHandler(BaseHTTPRequestHandler):

    def respond_data(self, data):
        data_json_bytes = (json.dumps(data) + '\n').encode('utf-8')
        self.wfile.write(data_json_bytes)

    def do_GET(self):

        global server_start_time

        if self.path == '/status':
            print('Received Request')
            print(self.client_address)
            self.send_response(200)
            self.send_header('Content-type:', 'text/html')
            self.end_headers()

            print('address_string')
            print(self.address_string())

            data = {'status': 'running'}
            self.respond_data(data)
            # data_json_bytes = ('\n' + json.dumps(data) + '\n').encode('utf-8')
            # self.wfile.write(data_json_bytes)

        elif self.path == '/uptime':
            print("Uptime heartbeat received")
            print(self.client_address)
            self.send_response(200)
            self.send_header('Content-type:', 'text/html')
            self.end_headers()
            now = datetime.datetime.now()
            uptime = str(now - server_start_time)

            data = {'status': 'running', 'uptime': uptime}
            self.respond_data(data)

        else:
            print('Received different request')


def run_mate_service(port, addr=''):
    class MateServer(threading.Thread):
        def run(self):
            httpd = HTTPServer((addr, port), MateRequestHandler)
            httpd.serve_forever()

    t = MateServer()
    t.daemon = True
    t.start()



