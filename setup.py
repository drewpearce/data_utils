import configparser
import os
from setuptools import setup

config = configparser.ConfigParser()
config.readfp(open('setup.cfg'))

os.environ['PBR_VERSION'] = config.get('metadata', 'version')
os.environ['SKIP_GENERATE_RENO'] = 'true'
os.environ['SKIP_GENERATE_AUTHORS'] = 'true'
os.environ['SKIP_WRITE_GIT_CHANGELOG'] = 'true'

setup_requires = [
    'pbr>=1.9',
    'setuptools>=17.1',
    'wheel'
]

setup(setup_requires=setup_requires, pbr=True)
