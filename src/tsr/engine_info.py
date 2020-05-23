'''
Created on Mar 7, 2020

@author: ballance
'''
from tsr.info import Info
from typing import List
from tsr.plusarg_info import PlusargInfo

class EngineInfo(Info):
    
    def __init__(self, name, mkfile, plusargs : List[PlusargInfo] = None):
        super().__init__(name, mkfile, plusargs)
        pass
    