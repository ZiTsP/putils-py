'''
Created on Nov 15, 2017

@author: zitsp
'''

from collections.abc import Iterable as iter
import uuid

from . import ptime

def flatten2list(*somethings, **opt):
    trim = opt.get('trim', False)
    _list = []
    for o in somethings:
        if isinstance(o, iter) and not isinstance(o, str):
            _list.extend(flatten2list(*o))
        else:
            _list.append(o)
    if trim is True:
        _list = [e for e in _list if not e == '' and not e == None]
    return _list

def reversed_list(list_):
    return list_[::-1]

def gen_timestamp():
    return str(ptime.gen_timestamp())

def gen_randname():
    return str(uuid.uuid4())


class Verify():

    @staticmethod
    def is_iterable(obj):
        return True if isinstance(obj, iter) and not isinstance(obj, str) else False


class DictInDict():
    @staticmethod
    def update_from_tuple(parentkey_value_tuple, child_key, dict_dict=None):
        if not isinstance(parentkey_value_tuple, tuple):
            return dict_dict
        if dict_dict is not None:
            m_dict = dict(dict_dict)
            for parent_key,value in parentkey_value_tuple:
                if parent_key in m_dict and isinstance(m_dict[parent_key], dict):
                    m_dict[parent_key].update({child_key : value})
                else:
                    m_dict[parent_key] = {child_key : value}
            return m_dict
        else:
            return {parent_key : {child_key : value} for parent_key, value in parentkey_value_tuple}

    @staticmethod
    def merge(*key_dict_iter):
        if len(key_dict_iter) <=1:
            return key_dict_iter[0]
        if isinstance(key_dict_iter[0], dict):
            m_dict = key_dict_iter[0]
        elif isinstance(key_dict_iter[0], list) and isinstance(key_dict_iter[0][0], tuple):
            m_dict = {k : v for k, v in key_dict_iter[0]}
        else:
            return
        for i in key_dict_iter[1:]:
            if isinstance(i, dict):
                iter_ = i.items()
            elif isinstance(i, list) and isinstance(i[0], tuple):
                iter_ = i
            else:
                continue
            for k,d in iter_:
                if not isinstance(d, dict):
                    continue
                if k in m_dict and isinstance(m_dict[k], dict):
                    m_dict[k].update(d)
                else:
                    m_dict[k] = d
        return m_dict

    @staticmethod
    def omit(dict_dict, *succeed_keys):
        if not isinstance(dict_dict, dict):
            raise(TypeError)
        keys = flatten2list(succeed_keys)
        return {parent_key : {k:value_dict[k] for k in keys if k in value_dict
            } for parent_key, value_dict in dict_dict.items()}

class ListInDict():
    @staticmethod
    def update_from_tuplelist(parentkey_value_tuples, list_in_dict=None):
        if not Verify.is_iterable(parentkey_value_tuples):
            return list_in_dict
        m_dict = dict(list_in_dict) if list_in_dict is not None else {}
        for parent_key,value in parentkey_value_tuples:
            if parent_key in m_dict and isinstance(m_dict[parent_key], list):
                m_dict[parent_key].append(value)
            else:
                m_dict[parent_key] = [value]
        return m_dict

    @staticmethod
    def merge(*key_list_iter):
        if len(key_list_iter) <=1:
            return key_list_iter[0]
        if isinstance(key_list_iter[0], dict):
            m_dict = key_list_iter[0]
        elif isinstance(key_list_iter[0], list) and isinstance(key_list_iter[0][0], tuple):
            m_dict = {k : v for k, v in key_list_iter[0]}
        else:
            return
        for itr in key_list_iter[1:]:
            if isinstance(itr, dict):
                iter_ = itr.items()
            elif isinstance(itr, list) and isinstance(itr[0], tuple):
                iter_ = itr
            elif isinstance(itr, tuple):
                iter_ = (itr)
            else:
                continue
            for k,d in iter_:
                if not isinstance(d, list):
                    continue
                if k in m_dict and isinstance(m_dict[k], list):
                    m_dict[k].append(d)
                else:
                    m_dict[k] = [d]
        return m_dict



class StringMatch():

    def __init__(self, delimiter=''):
        self.delimiter = delimiter

    def forward(self, *str_list):
        return StringMatch.forward_match(str_list, self.delimiter)

    def backward(self, *str_list):
        return StringMatch.backward_match(str_list, self.delimiter)

    @staticmethod
    def forward_match(str_list, delimiter=''):
        _list = flatten2list(str_list)
        if len(_list) <= 1:
            return _list[-1]
        dlist = [[c for c in s] for s in _list] if delimiter == '' else [
                s.split(delimiter) for s in _list]
        for i, p in enumerate(zip(*dlist)):
            if len(set(p)) <= 1:
                continue
            else:
                return delimiter.join(dlist[0][:i])
        min_len = min([len(e) for e in dlist])
        return delimiter.join(dlist[0][:min_len])

    @staticmethod
    def backward_match(str_list, delimiter=''):
        _list = flatten2list(str_list)
        if len(_list) <= 1:
            return _list[-1]
        dlist = [[c for c in s] for s in _list] if delimiter == '' else [
                s.split(delimiter) for s in _list]
        rlist = [reversed_list(e) for e in dlist]
        for i, p in enumerate(zip(*rlist)):
            if len(set(p)) <= 1:
                continue
            else:
                return delimiter.join(dlist[0][-i:])
        min_len = min([len(e) for e in dlist])
        return delimiter.join(dlist[0][-min_len:])
