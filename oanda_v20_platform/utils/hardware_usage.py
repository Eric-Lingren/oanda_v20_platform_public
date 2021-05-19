# %%
import psutil
import logging
logger = logging.getLogger(__name__)

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent()
    logger.info(f'cpu usage is: {cpu_usage}')
    return cpu_usage

def check_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    logger.info(f'memory usage is: {memory_usage}')
    return memory_usage
    
# %%
