
# used to generate package info and to enable pytest to function correctly 
# https://docs.pytest.org/en/6.2.x/goodpractices.html#goodpractices
from setuptools import setup, find_packages

setup(name="oanda_v20_platform_public", 
    packages=find_packages(where='oanda_V20_platform', exclude='tests'), 
    package_dir={"":"oanda_v20_platform"})