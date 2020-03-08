'''
Created on Mar 8, 2020

@author: ballance
'''

class RunCtxt(object):
    """Collects information about what is being run"""
    
    def __init__(self):
        self.project_name = None
        self.engine = None
        self.tools = []