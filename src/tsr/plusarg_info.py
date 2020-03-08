'''
Created on Mar 7, 2020

@author: ballance
'''
from enum import Enum, auto

class PlusargType(Enum):
    Int = auto()
    Str = auto()
    Time = auto()

class PlusargInfo(object):
    
    def __init__(self, name, description, arg_type=None):
        self.name = name
        self.description = description
        self.arg_type = arg_type
        