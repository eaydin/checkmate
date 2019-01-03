import socket
import threading
import time


def tcp_checker(address, port, close=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((address, port))
        s.shutdown(close)
        print("Success connecting to {addr}:{port}".format(addr=address, port=port))
        return True
    except socket.error as err:
        print("Socket error connecting to {addr}:{port} - {err}".format(addr=address, port=port, err=str(err)))
        return False
    except Exception as err:
        print("Unknown error connecting to {addr}:{port} - {err}".format(addr=address, port=port, err=str(err)))
        return False


def tcp_check(addresses, close=2, timer=10):
    while True:
        for addr_port in addresses:
            print('ADDR_PORT:', addr_port)
            if ':' not in addr_port:
                print('Error: Port not specified on address: {addr}'.format(addr=addr_port))
            else:
                addr = addr_port.split(':')[0]
                port = int(addr_port.split(':')[1])

                tcp_checker(addr, port, close)

        time.sleep(timer)


def run_tcp_check(addresses, close=2, timer=10):
    print('Starting TCP Checking for addresses')
    print(addresses)

    t = threading.Thread(target=tcp_check, args=[addresses, close, timer])
    t.daemon = True
    t.start()
