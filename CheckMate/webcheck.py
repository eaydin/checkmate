import urllib.request
import urllib.error
import time
import threading


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
