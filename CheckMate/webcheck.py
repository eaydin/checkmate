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
