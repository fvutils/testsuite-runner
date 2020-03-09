'''
Created on Mar 8, 2020

@author: ballance
'''
import os

class RunCtxt(object):
    """Collects information about what is being run"""
    
    def __init__(self):
        self.rundir = None
        self.launch_dir = None
        self.project = None
        self.engine = None
        self.engine_info = None
        self.tools = []
        self.tool_info = []
        
    def add_tool(self, tool):
        if tool not in self.tools:
            self.tools.append(tool)
            
    def get_builddir(self):
        return os.path.join(
            self.rundir, 
            self.project, 
            self.engine)
            