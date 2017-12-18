'''

pcc - private console control

- ConsolePrint (Bold, Thin, etc... and FontColor)
    ```cc_print("Message", SGRParameters [SGRParameters...])```

- CursolMove (Move, Erase, etc...)
    ```cc_move(CSISequence, n [n])

Created on Dec 6, 2017

@author: zitsp
'''

import sys
from enum import Enum

from . import putil


class ControlCodeError(Exception):
    pass

class _CSICode(Enum):
    ASCII_ESC_CODE_16 = '\x1b'
    ASCII_ESC_CODE_8 = '\033'

    @staticmethod
    def to_str(code : str):
        return _CSICode.ASCII_ESC_CODE_16.value + '[' + code


class CSISequence(Enum):

    CURSOR_UP = ('%dA', 1)
    CURSOR_DOWN = ('%dB', 1)
    CURSOR_LEFT = ('%dC', 1)
    CURSOR_RIGHT = ('%dD', 1)
    CURSOR_NEXT_LINE = ('%dE', 1)
    CURSOR_PREVIOUS_LINE = ('%dF', 1)
    CURSOR_HORIZONTAL_ABSOLUTE = ('%dG', 1)
    CURSOR_POSITION = ('%d;%dH', 2)
    ERASE_IN_DISPLAY_AFTER = ('0J', 0)
    ERASE_IN_DISPLAY_BEFORE = ('1J', 0)
    ERASE_IN_DISPLAY_ALL = ('2J', 0)
    ERASE_IN_LINE_AFTER = ('0K', 0)
    ERASE_IN_LINE_BEFORE = ('1K', 0)
    ERASE_IN_LINE_ALL = ('2K', 0)
    SCROLL_UP = ('%dS', 1)
    SCROLL_DOWN = ('%dT', 1)

    def to_str(self, *n):
        _n = putil.flatten2list(n)
        _less = self.value[1] - len(_n)
        if _less < 0:
            raise(ControlCodeError('There are too many arguments'))
        elif not all(isinstance(e, int) for e in _n):
            raise(ControlCodeError('There are not integer arguments'))
        elif 0 < _less:
            _n.extend([0]*_less)
        return self.value[0] % tuple(_n)

class SGRParameters(Enum):
    DEFAULT = 0
    BOLD = 1
    THIN = 2
    ITALIC = 3
    UNDER_LINE = 4
    BLINK = 5
    INVISIBLE = 8
    STRIKETHROUGH = 9
    FONT_BLACK = 30
    FONT_RED = 31
    FONT_GREEN = 32
    FONT_YELLOW = 33
    FONT_BLUE = 34
    FONT_MAGENTA = 35
    FONT_CYAN = 36
    FONT_WHITE = 37
    FONT_DEFAULT = 39
    BACKGROUND_BLACK = 40
    BACKGROUND_RED = 41
    BACKGROUND_GREEN = 42
    BACKGROUND_YELLOW = 43
    BACKGROUND_BLUE = 44
    BACKGROUND_MAGENTA = 45
    BACKGROUND_CYAN = 46
    BACKGROUND_WHITE = 47
    BACKGROUND_DEFAULT = 49

    def to_str(self):
        return '%d' %self.value

    @staticmethod
    def to_code(*sgr_codes):
        _codes = putil.flatten2list(sgr_codes)
        return _CSICode.to_str(';'.join([e.to_str() for e in _codes]) + 'm')

    @staticmethod
    def end_code():
        return _CSICode.to_str(SGRParameters.to_code(SGRParameters.DEFAULT))

def cc_print(str_ : str, *params : SGRParameters, **opts):
    end = opts.get('end', None)
    export_file = opts.get('export_file', None)
    error = opts.get('error', False)
    params = putil.flatten2list(params, trim=True)
    if not params:
        if error is True:
            print(str_, end=end, file=sys.stderr)
        else:
            print(str_, end=end)
    else:
        if export_file is not None:
            with open(export_file, 'a') as _export:
                print(str_, file=_export)
        elif params is not None:
            print(SGRParameters.to_code(params) + str_ + SGRParameters.end_code(), end=end)

def cc_move(code : CSISequence, *n):
    print(code.to_str(n))
