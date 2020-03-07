'''
Created on Sep 29, 2019

@author: ballance
'''

class TaskBase():
    
    def __init__(self):
        pass
    
    def run(self):
        raise Exception("run not implemented in task type \"" + str(type(self)) + "\"")