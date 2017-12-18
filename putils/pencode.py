'''
Created on Nov 28, 2017

@author: zitsp
'''

from enum import Enum

class CommonEncoding(Enum):
    UTF_8  = 0x10
    Latin_1 = 0x20
    ISO8859_1 = 0x21
    CP1251 = 0x40
    MS932 = 0x80
    Shift_JIS = 0x81
    CP1252 = 0x100
    GB2312 = 0x200
    EUC_KR = 0x400
    EUC_JP = 0x800
    GBK = 0x1000
    ISO8859_2 = 0x2000
    CP1250 = 0x4000
    ISO8859_15 = 0x8000
    CP1256 = 0x10000
    ISO8859_9 = 0x20000
    Big5 = 0x40000
    CP1254 = 0x80000
    CP874 = 0x100000


    def encode(self):
        return self.name

    def next_common(self):
        try:
            return CommonEncoding((self.value & 0xFFFFF0) << 1)
        except ValueError:
            return None

class EncodeErrors(Enum):
    RAISE_ERR = 'strict'
    IGNORE = 'ignore'
    REPLACE_NUM = 'backslashreplace' 
    REPLACE_STATIC_CHAR = 'replace'
    
def encode(str_ : str, to_encode=CommonEncoding.UTF_8 , errors=EncodeErrors.REPLACE_NUM):
    return str_.encode(to_encode.encode(), errors.value)