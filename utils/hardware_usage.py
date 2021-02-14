import psutil

def check_sys_usage():
    cpu_usage = psutil.cpu_percent()
    print(f'cpu usage is: {cpu_usage}')
    memory_usage = psutil.virtual_memory().percent
    print(f'memory usage is: {memory_usage}')