'''
Created on Sep 25, 2019

@author: ballance
'''
from unittest.suite import TestSuite

class VSuite(TestSuite):
    
    def __init__(self, name, suite=None, runner=None):
        self.name = name
        self.vsuite_l = []
        self.test_l = []
        pass

    def add_tests(self, path, pattern):
        pass
    
    def add_vsuite(self, path, runner=None):
        print("add_vsuite: " + str(path))
#        self.vsuite_l.append(VSuite(path, runner))
        pass
    
    def __str__(self):
        return "Hello"
        

