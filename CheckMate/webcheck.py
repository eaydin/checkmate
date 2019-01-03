import urllib.request
import urllib.error
import time
import threading
import json


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


def curl_checker(addresses, timer=10):

    while True:

        for address in addresses:
            t = curl_check(address)
            if t:
                print("Status of {addr}: {resp}".format(addr=address, resp=t.status))
        time.sleep(timer)


def run_curl_checker(addresses, timer=10):

    print('Start checking for addresses')
    print(addresses)

    t = threading.Thread(target=curl_checker, args=[addresses, timer])
    t.daemon = True
    t.start()


def mate_check_data(address_port):

    mate_address = 'http://{addr_port}/uptime'.format(addr_port=address_port)

    try:
        t = urllib.request.urlopen(mate_address)
        return t
    except urllib.error.HTTPError as err:
        print('HTTP error while checking mate {mate}: {err}'.format(mate=mate_address, err=str(err)))
        return False
    except Exception as err:
        print('Error while checking mate {mate}: {err}'.format(mate=mate_address, err=str(err)))
        return False


def mate_check(address_port, timer):

    while True:
        for addr_port in address_port:

            data = mate_check_data(addr_port)
            if not data:
                pass
            else:
                data_html = data.read()
                encoding = data.info().get_content_charset('utf-8')
                json_data = json.loads(data_html.decode(encoding))
                print('Response of heartbeat is')
                print(json_data)
        time.sleep(timer)


def run_mate_check(addresses, timer):

    print('Starting mate checking for addresses')
    print(addresses)

    t = threading.Thread(target=mate_check, args=[addresses, timer])
    t.daemon = True
    t.start()
