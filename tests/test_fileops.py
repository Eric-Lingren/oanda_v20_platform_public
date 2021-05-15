from utils.fileops import get_abs_path
from pathlib import Path

def test_get_abs_path():

    x = get_abs_path()
    assert x.is_file(), "Absolute path not generated correctly!"