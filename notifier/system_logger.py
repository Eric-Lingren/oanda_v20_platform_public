import logging
import os

def config_logger():
    log_name = 'log.txt'
    path = '../'
    log_filename = os.path.join(path, log_name)
    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename = log_filename, level=logging.DEBUG, format=LOG_FORMAT)
    logger = logging.getLogger()
    return logger

# logger.error(f'testing log error')
# logger.info(f'testing log info')
# logger.warning(f'testing log warning')