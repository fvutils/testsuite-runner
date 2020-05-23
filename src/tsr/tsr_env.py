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
        self.env["TSR_MKFILES_DIR"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "mkfiles")
        self.set_verbose(False)
        
    def set_verbose(self, v):
        self.env["VERBOSE"] = "true" if v else "false"
        
    