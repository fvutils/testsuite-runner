'''
Created on Mar 7, 2020

@author: ballance
'''

class Job(object):
    
    def __init__(self, name):
        self.job_rundir = None
        # Additional 
        self.env      = {}
        self.cmd      = []
        self.plusargs = []
        self.mk_includes = []
        
        # Name
        # Seed (?)
        # Run directory
        # 
        pass
    
