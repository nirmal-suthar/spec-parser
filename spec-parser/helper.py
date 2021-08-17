import os
import re
import logging
from os import path
from config import id_metadata_prefix


class ErrorFoundFilter(logging.Filter):
    def __init__(self):
        self.worst_level = logging.INFO

    def filter(self, record):
        if record.levelno > self.worst_level:
            self.worst_level = record.levelno
        return True


def isError():
    logger = logging.getLogger()
    for handler in logger.handlers:
        for filter in handler.filters:
            if isinstance(filter, ErrorFoundFilter):
                return filter.worst_level >= logging.ERROR
    return False


def safe_open(fname, *args):
    ''' 
    Open "fname" after creating neccessary nested directories as needed.
    '''

    dname = os.path.dirname(fname) if os.path.dirname(fname) != '' else './'
    os.makedirs(dname, exist_ok=True)
    return open(fname, *args)


def safe_listdir(dname):
    if path.exists(dname) and path.isdir(dname):
        return os.listdir(dname)
    return []


def union_dict(d1, d2):
    '''
    Concat two dict d1, d2. (inplace). Values in dict d1 will be given priority over dict d2.
    '''
    for k, v in d2.items():
        if not k in d1:
            d1[k] = v


def gen_rdf_id(entity, namespace_name):

    splitted = re.split(r':', entity)

    if len(splitted) > 2:
        return entity
    elif len(splitted) == 2:
        return f'{id_metadata_prefix}{splitted[0]}#{splitted[-1]}'
    else:
        return f'{id_metadata_prefix}{namespace_name}#{splitted[-1]}'