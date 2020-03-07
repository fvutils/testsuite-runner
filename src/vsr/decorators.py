'''
Created on Sep 29, 2019

@author: ballance
'''
from vsr.registry import Registry

def test(T):
    '''
    Registers a test configuration task
    '''
    print("Test: " + str(T))
    
    return T

class flow():
    '''
    Registers a flow class with VSR
    '''
    def __init__(self, name):
        self.name = name
        pass
    
    def __call__(self, T):
        Registry.inst().register_flow(self.name, T)
        return T
    

