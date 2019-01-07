import signal
import datetime
from CheckMate.webcheck import run_curl_checker
from CheckMate.mate import run_mate_service
from CheckMate.webcheck import run_mate_check
from CheckMate.tcp_check import run_tcp_check
import CheckMate.mate
import CheckMate.log
import argparse


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

    parser.add_argument('--debug-log', help='Path to debug log file.', default='/var/log/checkmate/checkmate.log',
                        metavar='<log_path>', required=False)
    parser.add_argument('--error-log', help='Path to error log file.', default='/var/log/checkmate/error.log',
                        metavar='<log_path>', required=False)

    args = parser.parse_args()

    # DEBUG logging

    try:
        debug_handler = CheckMate.log.logging.FileHandler(args.debug_log)
        debug_handler.setLevel(CheckMate.log.logging.DEBUG)
        debug_handler.setFormatter(CheckMate.log.formatter)
        CheckMate.log.logger.addHandler(debug_handler)

    except Exception as err:
        CheckMate.log.logger.error('Error while writing to debug log file: {0}'.format(str(err)))

    # ERROR logging

    try:
        error_formatter = CheckMate.log.logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d %(message)s')
        error_handler = CheckMate.log.logging.FileHandler('/var/log/checkmate/error.log')
        error_handler.setLevel(CheckMate.log.logging.ERROR)
        error_handler.setFormatter(error_formatter)
        CheckMate.log.logger.addHandler(error_handler)

    except Exception as err:
        CheckMate.log.logger.error('Error while writing to error log file: {0}'.format(str(err)))

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


