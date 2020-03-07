'''
Created on Sep 29, 2019

@author: ballance
'''

class Test():
    
    def __init__(self, name):
        self.name = name
        self.runarg_l = []
        
    def add_runarg(self, arg):
        self.runarg_l.append(arg)
        