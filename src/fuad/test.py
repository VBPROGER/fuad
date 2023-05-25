#!/usr/bin/env python3
import unittest
from os.path import join
from fuad.reader import Reader
from fuad.magic import magic
from fuad.constants import *

class TestFUAD(unittest.TestCase):
    file_data: str = ''
    test_file: str = join('src', 'assets', 'test.fuad')
    def setUp(self, *args, **kwargs):
        # with open(self.test_file, 'w+') as f:
            # f.write(magic['file']['start'])
        with open(self.test_file, 'r') as f:
            self.file_data = f.read()
    def test_Reader(self):
        r = Reader(self.file_data)
        r.run_all()
        self.assertEqual(len(r.get_all_list), 3)
        try:
            meta = r.get_meta('text.txt')['123']
        except KeyError: meta = {'name': 'unnamed'}
        else:
            print('KeyError was not called.')
            exit(1)
        self.assertIsNotNone(meta)
        self.assertIsNotNone(meta.get('name'))
        del meta
        self.assertIsNotNone(r.get_file_content('text.txt'))
        self.assertRaises(IsADirectoryError, r.get_file_content, 'afolder')
        self.assertTrue(r.is_dir('afolder'))
        self.assertFalse(r.is_file('afolder'))
        self.assertTrue(r.is_file('text.txt'))
        self.assertFalse(r.is_dir('cool.txt'))
        print('`text.txt` file content:', r.get_file_content('text.txt'))
        print('binary representation:', r.to_bin)

        print('\nstarting next test')
        r = Reader(empty_fuad_file)
        r.run_all()
        r.data = r.to_bin
        r.run_all()
        r.add_file('hello.txt', 'world')
        r.add_directory('sup')
        print('binary representatoin:', r.to_bin)

if __name__ == '__main__':
    unittest.main()
