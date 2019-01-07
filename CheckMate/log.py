import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Print to stdout

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

# DEBUG logging to checkmate.log

try:
    fh = logging.FileHandler('/var/log/checkmate/checkmate.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

except Exception as err:
    logger.error('Error while writing to debug log file: {0}'.format(str(err)))


# ERROR logging to error.log

try:
    error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d %(message)s')
    error_handler = logging.FileHandler('/var/log/checkmate/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)

except Exception as err:
    logger.error('Error while writing to error log file: {0}'.format(str(err)))

