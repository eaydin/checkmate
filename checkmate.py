import signal
import datetime
from CheckMate.webcheck import run_curl_checker
from CheckMate.mate import run_mate_service
import CheckMate.mate

if __name__ == '__main__':
    CheckMate.mate.server_start_time = datetime.datetime.now()

    run_mate_service(5555)
    run_curl_checker('https://veritech.net')

    signal.pause()

