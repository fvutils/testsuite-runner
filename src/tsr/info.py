'''
Created on Mar 7, 2020

@author: ballance
'''
from tsr.messaging import warn

class Info(object):
    
    def __init__(self, name, mkfile):
        self.rgy = None
        self.loaded = False
        self.name = name
        self.mkfile = mkfile
        self.plusargs = []
        self.description = ""
        
    def add_plusarg(self, plusarg):
        if not plusarg.name in map(lambda p:p.name, self.plusargs):
            self.plusargs.append(plusarg)
        else:
            warn("Duplicate plusarg \"" + plusarg.name + "\" in " + self.name)
            
    def load_info(self):
        if not self.loaded:
            self.rgy._load_info(self)
            self.loaded = True
            
        