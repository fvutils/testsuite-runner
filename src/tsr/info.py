'''
Created on Mar 7, 2020

@author: ballance
'''
from tsr.messaging import warn
from typing import List
from tsr.plusarg_info import PlusargInfo

class Info(object):
    
    def __init__(self, name, mkfile, plusargs : List[PlusargInfo] = None):
        self.rgy = None
        self.name = name
        self.mkfile = mkfile
        self.plusargs : List[PlusargInfo] = []
        self.loaded = False
        if plusargs is not None:
            for p in plusargs:
                self.add_plusarg(p)
            self.loaded = True
        self.description = ""
        
    def add_plusarg(self, plusarg : PlusargInfo):
        if not plusarg.name in map(lambda p:p.name, self.plusargs):
            self.plusargs.append(plusarg)
        else:
            warn("Duplicate plusarg \"" + plusarg.name + "\" in " + self.name)
            
    def load_info(self):
        if not self.loaded:
            self.rgy._load_info(self)
            self.loaded = True
            
        