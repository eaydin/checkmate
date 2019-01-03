import signal
import datetime
from CheckMate.webcheck import run_curl_checker
from CheckMate.mate import run_mate_service
from CheckMate.webcheck import run_mate_check
import CheckMate.mate
import argparse


if __name__ == '__main__':

    description = """Checkmate for various network connectivity by Veriteknik"""

    parser = argparse.ArgumentParser(prog='checkmate.py', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     fromfile_prefix_chars='@', description=description)
    parser.add_argument('--serve-mate', help='Serve HTTP Server with uptime and status, Specify TCP Port',
                        required=False, default=False, type=int)
    parser.add_argument('--webcheck', help='Domain (with protocol and port) to check via urllib. You can specify '
                                           'multiple domains separated with spaces.', nargs='+', default=False,
                        required=False)
    parser.add_argument('--webcheck-timer', help='Time to wait between each check, in seconds.', default=10,
                        required=False, type=int)

    parser.add_argument('--mate', help='Mate to check, with address and port. Ex: 192.168.30.5:4398, Checkmate will '
                                       'handle the protocol and paths. You can specify multiple mates separated '
                                       'with spaces.', nargs='+', default=False, required=False)

    parser.add_argument('--mate-timer', help='Timer to check mates.', default=5, required=False, type=int)

    args = parser.parse_args()

    start_status = False

    if not args.serve_mate and not args.webcheck and not args.mate:
        print('You should specify some arguments.')
        raise SystemExit(1)
    if args.serve_mate:
        CheckMate.mate.server_start_time = datetime.datetime.now()
        run_mate_service(args.serve_mate)
        start_status = True
    if args.webcheck:
        run_curl_checker(args.webcheck, args.webcheck_timer)
        start_status = True
    if args.mate:
        run_mate_check(args.mate, args.mate_timer)
        start_status = True

    if start_status:
        signal.pause()


