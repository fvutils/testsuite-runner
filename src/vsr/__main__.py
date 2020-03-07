'''
Created on Sep 24, 2019

@author: ballance
'''
import unittest
import os
import sys
import importlib
import vsr_core_flows
from vsr.suite_finder import SuiteFinder

for a in sys.argv:
    print("Arg: " + a)

finder = SuiteFinder()

finder.find(os.getcwd())


print("finder: " + str(finder))

# if os.path.isdir("testlists"):
#     os.sys.path.append("testlists")
#     for f in os.listdir("testlists"):
#         if f.endswith(".py"):
#             try:
#                 tl_m = importlib.import_module(f[:-3])
#                 
#                 if "suite" in dir(tl_m):
#                     print("Found a suite method")
#                     suite = tl_m.suite()
#                     print("suite=" + str(suite))
#                 else:
#                     print("Error: no 'suite' method")
#                     
#             except Exception as e:
#                 print("Error: " + str(e))
#                 pass
#         
        
    
#     loader = unittest.TestLoader()
#     tests = loader.discover("testlists", "*.py");
#     print("tests: " + str(tests))
#     
#     runner = unittest.TextTestRunner()
#     runner.run(tests)
