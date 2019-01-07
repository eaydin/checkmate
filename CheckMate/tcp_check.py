import socket
import threading
import time
from CheckMate.log import logger


def tcp_checker(address, port, close=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((address, port))
        s.shutdown(close)
        logger.info("tcp - Success connecting to {addr}:{port}".format(addr=address, port=port))
        # print("Success connecting to {addr}:{port}".format(addr=address, port=port))
        return True
    except socket.error as err:
        logger.error("tcp - Socket error connecting to {addr}:{port} - {err}".format(addr=address, port=port, err=str(err)))
        return False
    except Exception as err:
        logger.error("tcp - Unknown error connecting to {addr}:{port} - {err}".format(addr=address, port=port, err=str(err)))
        return False


def tcp_check(addresses, close=2, timer=10):
    while True:
        for addr_port in addresses:
            logger.debug("tcp - Checking {0}".format(addr_port))
            # print('ADDR_PORT:', addr_port)
            if ':' not in addr_port:
                logger.error('tcp - Port not specified on address: {addr}'.format(addr=addr_port))
            else:
                try:
                    addr = addr_port.split(':')[0]
                    port = int(addr_port.split(':')[1])

                    tcp_checker(addr, port, close)
                except Exception as err:
                    logger.error("tcp - Failed to check {0} due to an error: {1}".format(addr_port, str(err)))

        time.sleep(timer)


def run_tcp_check(addresses, close=2, timer=10):
    logger.debug('Starting TCP Checking for addresses: {0}'.format(" ".join(addresses)))

    t = threading.Thread(target=tcp_check, args=[addresses, close, timer])
    t.daemon = True
    t.start()
