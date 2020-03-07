'''
Created on Sep 27, 2019

@author: ballance
'''

class Suite():
    
    def __init__(self, name):
        self.name = name
        self.test_l = []
        self.suite_l = []
            
        print("Suite: " + self.name + " has " + str(len(self.test_l)))
        for t in self.test_l:
            id = t.id()
            id = id[id.rfind('.')+1:]
            print("Test: " + id)
            print("Result: " + str(t.run()))
        
    def collect_tests(self, test_l, matcher):
        s = TestSuite()
        
        
        
        
    