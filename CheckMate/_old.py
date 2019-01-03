import socket
import threading

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def listen(self, backlog=5, timeout=10):
        self.sock.listen(backlog)
        while True:
            client, address = self.sock.accept()
            client.settimeout(timeout)
            threading.Thread(target=self.handle_conn, args=(client, address)).start()

    def handle_conn(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    print("Received data: {0}".format(data))
                    response = data
                    client.send(data)
                else:
                    print("No data received?")
            except Exception as err:
                print("Error while recieving data: {0}".format(str(err)))
                client.close()
                return False

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    response = data
                    client.send(response)
                else:
                    print('client disconnected')
            except Exception as err:
                print("Error while receiving data: {0}".format(str(err)))
                client.close()
                return False





if __name__ == '__main__':
    # ThreadedServer('', 5555).listen()
    import heartbeat

    import time
    heartbeat.run_heartbeat_service(5555)

    time.sleep(500)
