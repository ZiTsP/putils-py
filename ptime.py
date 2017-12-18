'''
Created on Nov 16, 2017

@author: zitsp
'''

from datetime import datetime as time

def gen_timestamp(time_=None):
    return get_epoc_millisec(time_ if time_ is not None else time.now())
    
def now2str():
    return str(time.now())

def get_epoc_millisec(time_=None):
    time_ = time_ if time_ is not None else time.now()
    if isinstance(time_, time):
        return int(time_.timestamp() * 1000)
    else:
        return gen_timestamp()
    