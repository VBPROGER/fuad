#!/usr/bin/env python3
from fuad.utils import getchr

magic = {
    'file': {
        'start': f'FUAD//{getchr()}',
        'end': f'{getchr(1)}//FUAD'
    },
    'separators': {
        'data': getchr(2)
    }
}