'''
Created on May 16, 2020

@author: ballance
'''
from typing import List
from tsr.test import Test
from tsr.test_info import TestInfo
from tsr import messaging

class TestGroup(TestInfo):
    
    def __init__(self, name):
        super().__init__(name)
        self.testgroups : List['TestGroup'] = []
        self.tests : List[Test] = []
        
    def addTest(self, test : Test):
        test.parent = self
        self.tests.append(test)
        
    def findTests(self, spec : List[str])->List[TestInfo]:
        if spec[0] == "*" or spec[0] == "**":
            # Collect all groups and tests here
            ret = self.tests.copy()
            if len(spec) > 1 or spec[0] == "**":
                for g in self.testgroups:
                    ret.extend(g.findTests(
                        spec[1:] if len(spec) > 1 else ["**"]))
        else:
            # Look for a named element
            ret = []

            print("spec: " + str(spec) + " len=" + str(len(spec)))
            found = False
            if len(spec) > 1:
                # We're looking for a test group
                for g in self.testgroups:
                    if g.name == spec[0]:
                        ret.extend(g.findTests(spec[1:]))
                        found = True
                        break
            else:
                # We're selecting a test                        
                for t in self.tests:
                    if t.name == spec[0]:
                        ret.append(t)
                        found = True
                        break
                        
            if not found:
                messaging.error("Failed to find test element " + str(spec[0]))
                messaging.note("Available groups: " + " ".join(map(lambda t:t.name, self.testgroups)))
                messaging.note("Available tests: " + " ".join(map(lambda t:t.name, self.tests)))
                raise Exception("Failed to find test element " + str(spec[0]))
            
        return ret
        
    def findGroup(self, name : str, create=False)->'TestGroup':
        for g in self.testgroups:
            if g.name == name:
                return g
        if create:
            g = TestGroup(name)
            self.addTestGroup(g)
            
        return g
        
    def addTestGroup(self, testgroup : 'TestGroup'):
        testgroup.parent = self
        self.testgroups.append(testgroup) 