import json
import threading
import datetime
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from CheckMate.log import logger


class MateRequestHandler(BaseHTTPRequestHandler):

    def respond_data(self, data):
        data_json_bytes = (json.dumps(data) + '\n').encode('utf-8')
        self.wfile.write(data_json_bytes)

    def do_GET(self):

        global server_start_time

        if self.path == '/status':
            logger.info("mate - status request received from: {addr}".format(addr=self.client_address))
            self.send_response(200)
            self.send_header('Content-type:', 'text/html')
            self.end_headers()

            data = {'status': 'running'}
            self.respond_data(data)

        elif self.path == '/uptime':
            logger.info("mate - uptime heartbeat received from: {addr}".format(addr=self.client_address))
            self.send_response(200)
            self.send_header('Content-type:', 'text/html')
            self.end_headers()
            now = datetime.datetime.now()
            uptime = str(now - server_start_time)

            data = {'status': 'running', 'uptime': uptime}
            self.respond_data(data)

        else:
            logger.error('mate - Received different request')


def run_mate_service(port, addr=''):
    class MateServer(threading.Thread):
        def run(self):
            httpd = HTTPServer((addr, port), MateRequestHandler)
            httpd.serve_forever()

    t = MateServer()
    t.daemon = True
    t.start()



