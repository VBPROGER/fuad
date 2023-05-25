#!/usr/bin/env python3
import fuad.meta as meta
from fuad.meta import chmod_executable
from fuad.errors import *
from urllib.parse import quote as encode_url
from urllib.parse import unquote as decode_url
from html import unescape as decode_html_entities, escape as encode_html_entities
from toml import loads as load_toml, dumps as dump_toml # type: ignore
from hashlib import sha256 as hashing_method # You can change the hashing method, but be ready for compatibility issues
from os import getcwd, makedirs, remove as remove_file
from os.path import commonprefix, commonpath, realpath, abspath, relpath, join as join_paths, basename
from shutil import rmtree as remove_dir

getchr = lambda i = 0: stringize(chr(int(i) + 1000))
getchr.__doc__ = 'Get character by it\'s index in the unicode.'

stringize = lambda s = '': str(s)
stringize.__doc__ = 'Return object as a string.'

normalize = lambda s = '': stringize(s).lower().strip()
normalize.__doc__ = 'Normalize the string.'

decode_all = lambda s = '': decode_html_entities(decode_url(stringize(s)))
decode_all.__doc__ = 'Decode URL (`%20`) and HTML (`&amp;`) encoded entities.'

encode_all = lambda s = '': encode_url(stringize(s))
encode_all.__doc__ = 'Encode string to URL (`%20`).'

get_hash = lambda s = '': hashing_method(stringize(s).encode('utf-8')).hexdigest()
get_hash.__doc__ = 'Get hash (currently, {}) of the string.'.format(meta.hashing_method)

def secure_filename(fn: str = '', safe_directory: str = getcwd(), follow_symlinks: bool = True) -> str:
    '''Secure filename to prevent path traversal attack.
If path traversal is detected then error will be raised.'''
    if not fn: return fn
    if follow_symlinks: out = realpath(fn)
    else: out = abspath(fn)
    if (
        safe_directory != commonpath((safe_directory, out))
    ):
        raise InterceptedPath(
            'WARNING: Path was intercepted: \'{}\'/$FN with \'{}\'/SAFE and \'{}\'/OUT'
            .format
            (
                stringize(fn) or meta.unknown_symbol,
                stringize(safe_directory) or meta.unknown_symbol,
                stringize(out) or meta.unknown_symbol
            )
        )
    return relpath(out)
