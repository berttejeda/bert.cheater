import configparser as ConfigParser
import os
from setuptools import setup
import sysconfig
import sys

cfg = ConfigParser.ConfigParser()
cfg.read('setup.cfg')
my_package_name = cfg.get('metadata', 'name')

setup()
