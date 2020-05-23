'''
Created on May 16, 2020

@author: ballance
'''
from typing import List
from tsr.test import Test
from tsr.test_info import TestInfo

class TestGroup(TestInfo):
    
    def __init__(self, name):
        super().__init__(name)
        self.testgroups : List['TestGroup'] = []
        self.tests : List[Test] = []
        
    def addTest(self, test : Test):
        test.parent = self
        self.tests.append(test)
        
    def addTestGroup(self, testgroup : TestGroup):
        testgroup.parent = self
        self.testgroups.append(testgroup) 