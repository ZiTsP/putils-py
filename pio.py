'''
Created on Nov 15, 2017

@author: zitsp
'''

import os.path as path
import json
import re
from .putil import DictInDict
from .pencode import CommonEncoding

class Json():

    @staticmethod
    def read_json2dict(json_path):
        if path.exists(json_path):
            with open(json_path, 'r') as r:
                return json.load(r)

    @staticmethod
    def write_dict2json(dict_, json_path):
        if dict_ is not None and isinstance(dict_, dict):
            with open(json_path, 'w') as w:
                json.dump(dict_, w, sort_keys=True, indent=4)

class Csv():

    @staticmethod
    def read_csv2dict(csv_path, separator=',', header=True, column=True):
        if not path.exists(csv_path):
            raise(FileNotFoundError)
        _csv_lines = Files.read_lines(csv_path)
        _csv_lines = [e[:-1] for e in _csv_lines]
        if header is True:
            _columns = _csv_lines[0].split(separator) if column is True else None
            _csv_lines = _csv_lines[1:]
        else:
            _columns = None
        _dict = {}
        for line in _csv_lines:
            _line = line.split(separator)
            _key = _line[0]
            _val = _line[1:] if _columns is None else{
                _columns[i] : _line[i] for i in range(1, min([len(_columns), len(_line)]))}
            if isinstance(_dict.get(_key, None), dict):
                _dict[_key].update(_val)
            else:
                _dict[_key] = _val
        return _dict


    @staticmethod
    def write_dict2csv(from_dict, csv_path, separator=',', override=True):
        _to_columns = []
        for v in from_dict.values():
            if isinstance(v, dict):
                _to_columns.extend(v.keys())
        _to_columns = set(_to_columns)
        _to_col_len = len(_to_columns)
        _to_list = []
        for k,v in from_dict.items():
            if _to_col_len < 1:
                _v = v
            elif not isinstance(v, dict):
                _v = ['' * _to_col_len]
                _v.append(v)
            else:
                _v = [v.get(col, '') for col in _to_columns]
            _to_list.append((k,_v))
        _write_mode = 'w' if override is True else 'a'
        with open(csv_path, _write_mode) as writer:
            if 0 < _to_col_len and not (override is False and path.exists(csv_path)):
                _column = separator + separator.join(_to_columns)
                print(_column, file=writer)
            for k,v in _to_list:
                _line = k + separator + separator.join(v)
                print(_line, file=writer)

class Files():

    @staticmethod
    def read_lines(filepath, enc=CommonEncoding.UTF_8, trim=True):
        if enc is None:
            raise UnicodeDecodeError
        try:
            with open(filepath, 'r', encoding=enc.encode()) as tf:
                strs = [line.strip() if trim else line for line in tf]
                return strs
        except UnicodeDecodeError:
            return Files.read_lines(filepath, enc=enc.next_common(), trim=trim)

    @staticmethod
    def write_lines(lines_, path_, override=True, enc=CommonEncoding.UTF_8):
        _write_mode = 'w' if override is True else 'a'
        with open(path_, _write_mode, encoding=enc.encode()) as writer:
            for line in lines_:
                print(line, file=writer)

    @staticmethod
    def read_asbytes(filepath):
        with open(filepath, 'rb') as bf:
            return [b for b in bf.read()]

    @staticmethod
    def write_asbytes(bytes_, path_, override=True):
        _write_mode = 'wb' if override is True else 'ab'
        if isinstance(bytes_, bytes):
            with open(path_, _write_mode) as writer:
                writer.write(bytes_)

class ConvExport():

    @staticmethod
    def json2csv(from_path, to_path=None, separator=',', add=False):
        _ext_in = '.json'
        _ext_out = '.csv'
        if not path.exists(from_path):
            raise(FileNotFoundError)
        _to_path = re.sub(_ext_in + r'$', _ext_out, from_path) if to_path is None else to_path
        if not from_path.endswith(_ext_in) or not _to_path.endswith(_ext_out):
            raise(Exception('extension of input does not assure correct file type'))
        _from_dict = Json.read_json2dict(from_path)
        Csv.write_dict2csv(_from_dict, _to_path, separator, not add)
        return _to_path

    @staticmethod
    def csv2json(from_path, to_path=None, separator=',', header=True, column=True, add=False):
        _ext_in = '.csv'
        _ext_out = '.json'
        if not path.exists(from_path):
            raise(FileNotFoundError)
        _to_path = re.sub(_ext_in + r'$', _ext_out, from_path) if to_path is None else to_path
        if not from_path.endswith(_ext_in) or not _to_path.endswith(_ext_out):
            raise(Exception('extension of input does not assure correct file type'))
        _json_dict = Json.read_json2dict(_to_path) if add is True and path.exists(_to_path) else {}
        _from_dict = Csv.read_csv2dict(from_path, separator, header, column)
        _json_dict = DictInDict.merge(_json_dict, _from_dict)
        Json.write_dict2json(_json_dict, _to_path)
        return _to_path
