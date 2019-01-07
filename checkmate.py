import signal
import datetime
from CheckMate.webcheck import run_curl_checker
from CheckMate.mate import run_mate_service
from CheckMate.webcheck import run_mate_check
from CheckMate.tcp_check import run_tcp_check
import CheckMate.mate
import argparse
from CheckMate.log import logger


if __name__ == '__main__':

    description = """Checkmate for various network connectivity by Veriteknik"""

    parser = argparse.ArgumentParser(prog='checkmate.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     fromfile_prefix_chars='@', description=description)
    parser.add_argument('--serve-mate', help='Serve HTTP Server with uptime and status, Specify TCP Port',
                        required=False, default=False, type=int, metavar="<port>")
    parser.add_argument('--web-check', help='Domain (with protocol and port) to check via urllib. You can specify '
                                            'multiple domains separated with spaces.', nargs='+', default=False,
                        required=False, metavar="<domain_to_check>")
    parser.add_argument('--web-check-timer', help='Time to wait between each check, in seconds.', default=10,
                        required=False, type=int, metavar="<time>")

    parser.add_argument('--mate', help='Mate to check, with address and port. Ex: 192.168.30.5:4398, Checkmate will '
                                       'handle the protocol and paths. You can specify multiple mates separated '
                                       'with spaces.', nargs='+', default=False, required=False,
                                        metavar="<ip:port>")

    parser.add_argument('--mate-timer', help='Timer to check mates.', default=5, required=False, type=int,
                        metavar="<time>")

    parser.add_argument('--tcp-check', help='TCP Address/Ports to check. Ex: 192.168.70.40:443. You can specify '
                                            'multiple TCP Servers separated with spaces.', nargs='+', default=False,
                                            required=False, metavar="<ip:port>")
    parser.add_argument('--tcp-check-close', help='Time to close TCP connection (in seconds) before checking if open.',
                        default=2, required=False, type=int, metavar="<time>")
    parser.add_argument('--tcp-check-timer', help='Time to wait between each TCP check in seconds.', default=10,
                        required=False, type=int, metavar="<time>")

    args = parser.parse_args()

    start_status = False

    if not args.serve_mate and not args.web_check and not args.mate and not args.tcp_check:
        print('You should specify some arguments.')
        raise SystemExit(1)
    if args.serve_mate:
        CheckMate.mate.server_start_time = datetime.datetime.now()
        run_mate_service(args.serve_mate)
        start_status = True
    if args.web_check:
        run_curl_checker(args.web_check, args.web_check_timer)
        start_status = True
    if args.mate:
        run_mate_check(args.mate, args.mate_timer)
        start_status = True
    if args.tcp_check:
        run_tcp_check(args.tcp_check, args.tcp_check_close, args.tcp_check_timer)
        start_status = True

    if start_status:
        signal.pause()


