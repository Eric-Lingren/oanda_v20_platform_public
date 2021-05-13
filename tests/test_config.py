from config import args
import argparse
import configparser
    

def test_args():
    x = args.parse_args(["--bot=rsi_test", "--pair='EUR_USD'" ])
    message = "Parse args function is not reading args"
    assert isinstance(x, argparse.Namespace), message

# def test_config_ini():
#     config_local = configparser.ConfigParser()
#     config_local.read('../config/config.ini')
#     message = "Cant read config.ini file with config parser"
#     assert config_local.getboolean('Other', 'test'), message

