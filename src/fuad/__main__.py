#!/usr/bin/env python3
# raise NotImplementedError('CLI interface is not implemented yet')
import fuad.meta as meta
from sys import argv as arguments
from fuad.reader import *

if __name__ != '__main__':
    raise LookupError('Do not execute __main__.py file directly, use it as module (python3 -m {})'.format(
        meta.__name__,
    ))

def main(*args, **kwargs):
    '''Parse arguments'''
    if ('-v' in args or '--verbose' in args):
        print(args)
    try: archive_name = args[1]
    except IndexError: archive_name = 'archive.fuad'
    try: extract_to = args[2]
    except IndexError: extract_to = 'extracted'
    try:
        rd = FileReader(archive_name)
    except (FileNotFoundError, IsADirectoryError):
        raise FileNotFoundError('File does not exist.')
    rd.run_all()
    rd.extract_all(extract_to)
    ...

main(*arguments)