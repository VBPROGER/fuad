#!/usr/bin/env python3
from setuptools import setup, find_packages
from src.fuad.meta import (
    __name__ as package_name,
    __version__ as package_version
)

setup(
    name = package_name,
    version = package_version,
    author = 'VBPROGER',
    packages = find_packages(),
    package_dir = {'': 'src'},
    install_requires = ['toml>=0.10.2']
    # license = '...'
)
