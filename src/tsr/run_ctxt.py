'''
Created on Mar 8, 2020

@author: ballance
'''
import os
from typing import Set

class RunCtxt(object):
    """Collects information about what is being run"""
    
    def __init__(self):
        self.rundir = None
        self.launch_dir = None
        self.project_cfg = None
        self.engine = None
        self.engine_info = None
        self.tools : Set[str] = set()
        self.tool_info = []
        self.test_info = []
        self.regress_mode = False
        self.regress_id = "regression_id"
        
    def add_tool(self, tool):
        if tool not in self.tools:
            self.tools.append(tool)
            
    def get_builddir(self):
        return os.path.join(
            self.rundir, 
            self.project, 
            "none" if self.engine is None else self.engine)
        
    def get_testdir(self, testname, id):
        if self.regress_mode:
            return os.path.join(
                self.rundir, 
                self.project,
                "regress",
                self.regress_id,
                ("%s_%04d" % (testname,id)))
        else:
            return os.path.join(
                self.rundir, 
                self.project,
                "tests",
                testname
                )
            