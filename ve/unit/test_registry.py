'''
Created on Mar 7, 2020

@author: ballance
'''
from tsr_test_case import TsrTestCase
from tsr.registry import Registry
from tsr.messaging import set_verbosity

class TestRegistry(TsrTestCase):
    
    def test_smoke(self):
        set_verbosity(2)
        
        rgy = Registry()
        rgy.load()
        