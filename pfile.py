'''
Created on Nov 15, 2017

@author: zitsp
'''

import glob
import os
import shutil
import zipfile

import os.path as path
from putils import putil
from putils.pencode import CommonEncoding


def mkdir(path_, **opts):
    from putils.pcl import Commands
    dopts = opts.get('dopts', {})
    dopts.update(opts)
    Commands.mkdir(path_, dopts=dopts)
    
def chmod(path_, chmod_, **opts):
    from putils.pcl import Commands
    dopts = opts.get('dopts', {})
    dopts.update(opts)
    Commands.chmod(path_, chmod_, dopts=dopts)

def cp(from_path, to_path, **opts):
    from putils.pcl import Commands
    dopts = opts.get('dopts', {})
    dopts.update(opts)
    Commands.cp(from_path, to_path, dopts=dopts)

class Find():

    @staticmethod    
    def files(rootdir, recursive=True):
        return [f for f in Find.find(rootdir, '*',recursive=recursive) if path.isfile(f)]
    
    @staticmethod    
    def subdirs(rootdir, recursive=True):
        return [f for f in Find.find(rootdir, '*',recursive=recursive) if path.isdir(f)]
    
    @staticmethod    
    def find(rootdir, *expression, recursive=True):
        files = set()
        if rootdir is None or path.exists(rootdir) is False:
            raise FileNotFoundError
        for e in putil.flatten2list(expression):
            exp = path.join(rootdir if recursive is False else path.join(rootdir, '**'), e)
            files.update(glob.glob(exp, recursive=recursive))
        return list(files)
    
class Paths():
    
    @staticmethod    
    def get_abspath(path_):
        return Paths.to_absolute(path_)
    
    @staticmethod
    def get_dirname(path_):
        _path = Paths.get_abspath(path_)
        if path.exists(_path) and path.isdir(_path):
            return _path
        else:
            return path.dirname(_path)
    
    @staticmethod
    def get_filename(path_):
        return path.split(path_)[1]
    
    @staticmethod
    def get_parentname(path_):
        return path.split(path.split(path_)[0])[0]
    
    @staticmethod
    def split_name_and_ext(path_):
        return (path.splitext(path.split(path_)[1]))
    
    @staticmethod
    def split_name(path_):
        return Paths.split_name_and_ext(path_)[0]
    
    @staticmethod
    def split_ext(path_):
        return path.splitext(path_)[1]
    
    @staticmethod
    def to_relative(from_path, to_path):
        from_tree = path.abspath(from_path).split('/')
        to_tree = path.abspath(to_path).split('/')
        diff_len = [len(from_tree), len(to_tree)]
        for from_, to_ in zip(from_tree, to_tree):
            if from_ == to_:
                diff_len[0] -= 1
                diff_len[1] -= 1
                continue
            else:
                break
        re_path = './'
        re_path += '../' * diff_len[0]
        re_path += '/'.join(to_tree[-diff_len[1]:]) if diff_len[1] is not 0 else ''
        return re_path
        
    @staticmethod
    def to_absolute(path_):
        return path.abspath(path_)
    
    @staticmethod
    def is_same_path(path_a, path_b):
        _a = path.abspath(path_a)
        _b = path.abspath(path_b)
        return _a == _b
    
    @staticmethod
    def is_diff_path(path_a, path_b):
        return not Paths.is_same_path(path_a, path_b)

    @staticmethod
    def is_empty_dir(path_):
        if not path.exists(path_):
            raise(FileNotFoundError)
        elif not path.isdir(path_):
            raise(NotADirectoryError)
        elif not os.listdir(path_):
            return True
        else:
            return False
 
class Readers():
    
    @staticmethod
    def read_lines(filepath, enc=CommonEncoding.UTF_8):
        if enc is None:
            raise UnicodeDecodeError
        try:
            with open(filepath, 'r', encoding=enc.encode()) as tf:
                strs = [line for line in tf]
                return strs
        except UnicodeDecodeError:
            return Readers.read_lines(filepath, enc=enc.next_common())
    
    @staticmethod    
    def read_asbytes(filepath):
        with open(filepath, 'rb') as bf:
            return [b for b in bf.read()]

class Extract():
    
    @staticmethod
    def unzip(path_, to_dir=None, overrdie=False, errskip=True):
        print('unzip')
        if not path.exists(path_):
            if errskip:
                return
            raise(FileNotFoundError)
        if path.isdir(path_):
            if errskip:
                return
            raise(IsADirectoryError)
        from_name, from_ext = Paths.split_name_and_ext(path_)
        if not from_ext:
            raise(zipfile.BadZipFile)
        if to_dir is None:
            to_dir = path.splitext(path_)[0]
        elif not (from_name == Paths.get_dirname(path_)):
            to_dir = path.join(to_dir, from_name)
        if path.exists(to_dir) and not path.isdir(to_dir):
            raise(NotADirectoryError)
        try:
            if path.exists(to_dir):
                if overrdie is True:
                    shutil.rmtree(to_dir)
                else:
                    return to_dir
            mkdir(to_dir)
            zip_ref = zipfile.ZipFile(path_, 'r')
            zip_ref.extractall(to_dir)
            zip_ref.close()
            return to_dir
        except (zipfile.BadZipFile, NotADirectoryError) as err:
            if errskip:
                return
            raise(err)
    
    @staticmethod
    def unjar(path_, to_dir=None, overrdie=False, errskip=True):
        if not path.splitext(path_)[1] == '.jar':
            if errskip:
                return
            raise(Extract.BadJarFile("not '*.jar' file"))
        Extract.unzip(path_, to_dir=to_dir, overrdie=overrdie, errskip=errskip)
        
    class BadJarFile(Exception):
        pass
