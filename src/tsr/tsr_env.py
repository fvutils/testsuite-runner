'''
Created on Mar 8, 2020

@author: ballance
'''
import os
import sys

class TsrEnv(object):
    
    def __init__(self):
        self.env = os.environ.copy()
        self.env["TSR_PYTHON"] = sys.executable
        self.env["VERBOSE"] = "true"
        
    