'''
Created on Sep 27, 2019

@author: ballance
'''

class TestSet():
    
    def __init__(self, test_m):
        self.name = type(test_m).__name__
        self.test_l = []
        
        for m in dir(test_m):
            if m.startswith("test_") and callable(getattr(test_m, m)):
                print("Found a test: " + str(m))
                tm = getattr(test_m, m)
                self.test_l.append(tm)
                tm()
        