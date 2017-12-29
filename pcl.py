'''

pcl - private command line (actions)

    Especially, to makes something effect or to use something external

- RunCommand
    ```exe_cmd()```

- Commands class
    ```Commands.mkdir(), Commands.chmod(), Comands.cd()...```

Created on Nov 15, 2017

@author: zitsp
'''

from collections import abc
import os
import os.path as path
import shutil
import subprocess

from . import pcc
from . import ptime
from . import putil
from .pfile import Paths


PATH_HERE = './'

DEBUG = True

def exe_cmd(cmd, execute_dir=None, sub_cmd=None, **opts):
    dopts = opts.get('dopts', {})
    dopts.update(opts)
    print_subprocess = dopts.get('print_subprocess', False)
    print_cmd = dopts.get('print_cmd', DEBUG)
    log_file = dopts.get('log_file', None)
    if isinstance(cmd, str):
        _cmd = cmd.split()
    elif isinstance(cmd, abc.Iterable):
        _cmd = putil.flatten2list(cmd)
    else:
        return
    current_dir = os.getcwd()
    execute_dir = os.getcwd() if execute_dir is None else execute_dir
    diff_path_flag = Paths.is_diff_path(os.getcwd(), execute_dir)
    if diff_path_flag:
        Logger.print_cmd(('cd', Paths.to_relative(os.getcwd(), execute_dir)), start_subprocess=True, dopts=dopts)
        dopts['start_subprocess'] = False
        dopts['end_subprocess'] = True
        os.chdir(execute_dir)
    try:
        if log_file is not None and print_subprocess is True:
            with open(log_file, 'a') as _log:
                subprocess.run(_cmd, check=True, stdout=_log, stderr=subprocess.STDOUT)
        else:
            (_stdout, _stderr) = (None, None)
            if print_subprocess is False:
                (_stdout, _stderr) = (subprocess.PIPE, subprocess.PIPE)
            subprocess.run(_cmd, check=True, stdout=_stdout, stderr=_stderr)
            Logger.print_cmd(_cmd, dopts=dopts)
    except subprocess.CalledProcessError:
        if sub_cmd is not None:
            exe_cmd(sub_cmd, execute_dir, dopts=dopts)
        elif print_subprocess is False or print_cmd is True:
            log_msg = 'ERROR: %s : %s' % (ptime.now2str(),' '.join(_cmd))
            Logger.print_cmd(log_msg, error=True, dopts=dopts)
    if diff_path_flag:
        os.chdir(current_dir)

class Commands():

    @staticmethod
    def mkdir(path_, **opts):
        dopts = opts.get('dopts', {})
        dopts.update(opts)
        chmod_ = dopts.get('chmod', None)
        mkdirs_ = dopts.get('recursive', False)
        _path = Paths.to_absolute(path_)
        _msg = ['mkdir']
        if path.exists(_path):
            return
        elif mkdirs_ is True and not path.exists(Paths.get_dirname(_path)):
            os.makedirs(_path)
            _msg.append('-p')
        else:
            os.mkdir(_path)
        Logger.print_cmd((_msg, path_), dopts)
        return Commands.chmod(path_, chmod_=chmod_)

    @staticmethod
    def chmod(path_, chmod_=None, **opts):
        dopts = opts.get('dopts', {})
        dopts.update(opts)
        if chmod_ is not None:
            os.chmod(path_, chmod_)
            Logger.print_cmd(('chmod', chmod_, path_), dopts)
        return path_

    @staticmethod
    def cd(to_path, **opts):
        dopts = opts.get('dopts', {})
        dopts.update(opts)
        from_path = os.getcwd()
        if Paths.is_diff_path(from_path, to_path):
            os.chdir(to_path)
            Logger.print_cmd(('cd', Paths.to_relative(from_path, to_path)), dopts)
        return (from_path, to_path)

    @staticmethod
    def cp(from_path, to_path, **opts):
        dopts = opts.get('dopts', {})
        dopts.update(opts)
        if not path.exists(from_path):
            raise(FileNotFoundError)
        if not path.isdir(from_path):
            to_dir = Paths.get_dirname(to_path)
            if Paths.is_same_path(to_dir, to_path):
                to_path = path.join(to_dir, Paths.get_filename(from_path))
            if not path.exists(to_dir):
                Commands.mkdir(to_dir, recursive=True)
            shutil.copyfile(from_path, to_path)
        else:
            if path.exists(to_path):
                raise(FileExistsError)
            shutil.copytree(from_path, to_path)
        Logger.print_cmd(('cp', from_path, to_path), dopts)


class Logger():

    ERR_COLOR = pcc.SGRParameters.FONT_RED

    @staticmethod
    def print_cmd(cmd, error=False, enable_print=True, **opts):
        dopts = opts.get('dopts', {})
        dopts.update(opts)
        log_file = dopts.get('log_file', None)
        start_subprocess = dopts.get('start_subprocess', False)
        end_subprocess = dopts.get('end_subprocess', False)
        err_redirect = dopts.get('err_redirect', False)
        if enable_print is False and log_file is None:
            pass
        else:
            cmd = putil.flatten2list(cmd)
            cmd_ = ' '.join(cmd) if 1 < len(cmd) else cmd
            if start_subprocess is True and end_subprocess is True:
                (str_, end_) = ('%s: (%s)' % (ptime.now2str(), cmd_), None)
            elif start_subprocess is True:
                (str_, end_) = ('%s: (%s' % (ptime.now2str(), cmd_), ' && ')
            elif end_subprocess is True:
                (str_, end_) = ('%s)' % cmd_, None)
            else:
                (str_, end_) = ('%s: %s' % (ptime.now2str(), cmd_), None)
            param = Logger.ERR_COLOR if err_redirect is True else None
            pcc.cc_print(str_, param, end=end_, export_file=log_file, error=error)

    @staticmethod
    def println(str_, error=False, enable_print=True):
        if enable_print is False:
            pass
        else:
            pcc.cc_print(str_, Logger.ERR_COLOR if error is True else None)
