'''
Created on Sep 24, 2019

@author: ballance
'''
import unittest
import os

if os.path.isdir("testlists"):
    loader = unittest.TestLoader()
    tests = loader.discover("testlists", "*.py");
    print("tests: " + str(tests))
    
    runner = unittest.TextTestRunner()
    runner.run(tests)
