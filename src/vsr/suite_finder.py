'''
Created on Sep 27, 2019

@author: ballance
'''
import importlib
import os
import unittest

from vsr.compound_suite import CompoundSuite
from vsr.suite import Suite
from vsr.testset import TestSet


class SuiteFinder():
    
    def __init__(self):
        self.compound_suite_l = []
        self.testset_l = []
        pass
    
    def find(self, rootdir):
        if os.path.isdir(os.path.join(rootdir, "tests")):
            for f in os.listdir(os.path.join(rootdir, "tests")):
                os.sys.path.append(os.path.join(rootdir, "tests"))
                if f.endswith(".py"):
                    try:
                        tl_m = importlib.import_module(f[:-3])
                    except Exception as e:
                        raise Exception("Failed to load module: " + str(e))
                        
                    if "suite" in dir(tl_m):
                        try:
                            suite = tl_m.suite()
                        except Exception as e:
                            raise Exception("Failed to load testlist file \"" + str(os.path.join(rootdir, "tests", f)) + "\": " + str(e))
                    else:
                        # Looks like a file of individual tests
                        self.testset_l.append(TestSet(tl_m))
                                    
                            