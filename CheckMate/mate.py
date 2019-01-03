import json
import threading
import datetime
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.error


class MateRequestHandler(BaseHTTPRequestHandler):

    def respond_data(self, data):
        data_json_bytes = ('\n' + json.dumps(data) + '\n').encode('utf-8')
        self.wfile.write(data_json_bytes)

    def do_GET(self):

        global server_start_time

        if self.path == '/status':
            print('Received Request')
            print(self.client_address)
            self.send_response(200)
            self.send_header('Content-type:', 'text/html')
            self.end_headers()
            now = datetime.datetime.now()

            print('address_string')
            print(self.address_string())


            data = {'status': 'running'}
            data_json_bytes = ('\n' + json.dumps(data) + '\n').encode('utf-8')
            self.wfile.write(data_json_bytes)

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


def curl_check(address):
    try:
        t = urllib.request.urlopen(address)
        return t
    except urllib.error.HTTPError as err:
        print("HTTP error while connecting to {addr}: {err}".format(addr=address, err=str(err)))
        return False
    except Exception as err:
        print("Unknown error while connecting to {addr}: {err}".format(addr=address, err=str(err)))
        return False


def curl_checker(address, timer=10):

    while True:
        t = curl_check(address)
        if t:
            print("Status of {addr}: {resp}".format(addr=address, resp=t.status))
        time.sleep(timer)


def run_curl_checker(address, timer=10):

    t = threading.Thread(target=curl_checker, args=[address, timer])
    t.daemon = True
    t.start()


if __name__ == '__main__':

    global server_start_time
    server_start_time =  datetime.datetime.now()

    import time
    import signal

    run_mate_service(5555)
    run_curl_checker('https://veritech.net')
    signal.pause()