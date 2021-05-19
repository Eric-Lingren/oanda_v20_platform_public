from utils.hardware_usage import check_memory_usage, check_cpu_usage
import socket
import pytest


def test_cpu_useage_stats():
    x = check_cpu_usage()
    message = "The check cpu usage function is not returning the expected value"
    assert isinstance(x, float), message
    assert x > 0, message

def test_memory_useage_stats():
    x = check_memory_usage()
    message = "The check memory usage function is not returning the expected value"
    assert isinstance(x, float), message
    assert x > 0, message


def test_internet_connection():
    message = "No connection to the internet, could not reach 1.1.1.1"
    with pytest.raises(Exception) as execinfo:   
        host = socket.gethostbyname("one.one.one.one")
        s = socket.create_connection((host, 80), 2)
        s.close()
        raise Exception(message)

    assert execinfo.value.args[0] == message
  
      
    
