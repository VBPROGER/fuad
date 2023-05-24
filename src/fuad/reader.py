#!/usr/bin/env python3
import fuad.meta as meta
from fuad.errors import *
from fuad.utils import *
from fuad.magic import magic

class Reader:
    '''{} Reader that accept raw string.'''.format(meta.__name__.upper())
    def __init__(self, data, *args, **kwargs):
        self.data = data
    def check_magic(self, *args, **kwargs):
        return self.data.startswith(magic['file']['start'])
    def remove_magic(self, *args, **kwargs):
        return self.data.removeprefix(magic['file']['start']).removesuffix(magic['file']['end'])
    def split_data(self, *args, **kwargs):
        return self.data.split(magic['separators']['data'])
    def turn_list_to_dict(self, index: int = 0, *args, **kwargs):
        return load_toml(self.data[index])
    def read(self, *args, **kwargs):
        '''Read data and parse it.'''
        new_data = self.data
        for index, _ in enumerate(self.data):
           new_data[index] = self.turn_list_to_dict(index)
        return new_data
    def run_all(self, *args, **kwargs):
        '''Run reader processes.'''
        if self.check_magic(): self.data = self.remove_magic()
        else: raise MagicError('Invalid magic')
        self.data = self.split_data()
        self.data = self.read()
        self.data = self._sort()
        self.data = self.sec_protect_paths()
        self.sec_check_file_hashes()
    def get_file_by_name(self, name: str = '') -> dict:
        return self.data[name]
    def get_meta(self, name: str = '') -> bool or dict:
        '''Get `meta` by name from `data`'''
        if name: return self.get_file_by_name(name)['meta']
        else: raise DataReadingError('Failed to read data')
    def get_meta_field(self, name: str = '', field: str = 'name', empty_ok: bool = False) -> any:
        got_meta = self.get_meta(name)
        if empty_ok: return got_meta.get(field)
        else: return got_meta[field]
    def get_raw_file_content(self, name: str = '') -> str:
        if self.is_file(name): return self.get_meta_field(name, 'content')
        else: raise IsADirectoryError('"{}" is a directory'.format(name))
    def get_file_content(self, name: str = '') -> str:
        return decode_all(self.get_raw_file_content(name))
    def get_file_type(self, name: str = '') -> bool:
        return normalize(self.get_meta_field(name, 'type'))
    def is_file(self, name: str = '') -> bool:
        return self.get_file_type(name) == 'file'
    def is_dir(self, name: str = '') -> bool:
        return not self.is_file(name)
    def extract_all(self, directory: str = '.') -> bool:
        self.sec_protect_paths()
        self.sec_check_file_hashes()
        exist_ok = (directory != '.')
        mode = 'x+' if not exist_ok else 'w+'
        for file_name in self.get_data_copy:
            old_fn = file_name
            file_name = join_paths(directory, file_name)
            if self.is_file(old_fn):
                with open(file_name, mode) as f:
                    f.write(self.get_file_content(old_fn))
            elif self.is_dir(old_fn):
                makedirs(file_name, chmod_executable, exist_ok = exist_ok)
            else:
                raise UnexpectedHandleError('Cannot extract the archive')
        return True
    def sec_check_file_hashes(self, *args, **kwargs) -> bool:
        for path in self.get_data_copy:
            self.sec_check_file_hash(path)
        return True
    def sec_check_file_hash(self, name: str = '') -> bool:
        if self.is_dir(name): return False
        source_hash = self.sec_get_file_hash_from_meta(name)
        if not source_hash: return False
        result_hash = self.sec_get_file_hash(name)
        if source_hash != result_hash:
            raise HashMismatch('Hashed mismatched: ({}/S) != ({}/R)'.format(source_hash, result_hash))
        return True
    def sec_protect_paths(self, *args, **kwargs) -> dict:
        new_data = self.get_data_copy
        for path in self.get_data:
            new_data = self.sec_protect_path(path, new_data)
        return new_data
    def sec_protect_path(self, name: str = '', _data: dict = {}, *args, **kwargs) -> dict:
        new_data = _data if _data else self.get_data_copy
        del _data
        new_name = secure_filename(name)
        new_data[new_name] = new_data.pop(name)
        new_data[new_name]['meta']['name'] = new_name
        return new_data
    def sec_get_file_hash(self, name: str = '', *args, **kwargs) -> str:
        return get_hash(self.get_file_content(name)) or meta.unknown_hash
    def sec_get_file_hash_from_meta(self, name: str = '', *args, **kwargs) -> str:
        return self.get_meta_field(name, 'hash', empty_ok = True) or False
    def _sort(self, *args, **kwargs):
        old_data = self.data
        new_data = {}
        for index, _ in enumerate(old_data):
            value = old_data[index]
            new_data[value['meta']['name']] = value
        return new_data
    @property
    def get_data(self):
        '''Readonly property to get `data`.'''
        return self.data
    @property
    def get_data_copy(self):
        '''Get copy of data to freely modify.'''
        return self.get_data.copy()
    @property
    def get_all_list(self):
        '''Readonly property to get list of files and directories'''
        return list(self.get_data.keys())
class FileReader(Reader):
    '''Reader that accepts file names.'''
    def __init__(self, fn, mode: str = 'r+',*args, **kwargs):
        with open(stringize(fn), stringize(mode) or 'r+') as f:
            self.data = f.read()