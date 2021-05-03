import logging
import os
from datetime import datetime

def config_logger():
    # get todays date
    datestamp = datetime.now().strftime('%Y%m%d')
    # use append date to logfile name
    log_name = f'log-{datestamp}.txt'
    path = './logs/'
    log_filename = os.path.join(path, log_name)
    # create log if it does not exist
    if not os.path.exists(log_filename):
            open(log_filename, 'w').close()
    # set log format
    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename = log_filename, level=logging.DEBUG, format=LOG_FORMAT)
    logger = logging.getLogger()
    return logger

# logger.error(f'testing log error')
# logger.info(f'testing log info')
# logger.warning(f'testing log warning')