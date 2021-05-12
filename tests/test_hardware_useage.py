from utils.hardware_usage import check_memory_usage, check_cpu_usage

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