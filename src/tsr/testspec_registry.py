'''
Created on May 23, 2020

@author: ballance
'''
import json
import os
from typing import List

from tsr.test_group import TestGroup
from tsr import messaging
from tsr.test_info import TestInfo


class TestspecRegistry(TestGroup):
    
    def __init__(self):
        super().__init__(None)
        
    def getTests(self, spec)->List[TestInfo]:
        """Returns tests matched by a given pattern"""
        spec_l = spec.split('.')
        
        return self.findTests(spec_l)
    
    def load_testspec(self, file):
        with open(file, "r") as fp:
            spec_j = json.load(fp)
            
            if "group" in spec_j.keys():
                # Just a single group in this file
                self.load_testgroup(spec_j["group"])
            elif "groups" in spec_j.keys():
                # Multplie groups in the same file
                for group in spec_j["groups"]:
                    self.load_testgroup(group)
            else:
                raise Exception("Neither 'group' nor 'groups' specified in file")
            
    def load_testgroup(self, group):
        if "name" not in group.keys():
            raise Exception("Error: group name not specified")
        
        name_path = group["name"].split(".")
        g = None
        for name in name_path:
            if g is None:
                g = self.findGroup(name, True)
            else:
                g = g.findGroup(name, True)
            if g is None:
                raise Exception("Failed to create group")
            
        if "variables" in group.keys():
            # TODO: load variables
            pass
        
        if "tests" in group.keys():
            for test in group["tests"]:
                self.load_test(g, test, group["tests"][test])
        else:
            messaging.warn("No tests")
            
        print("group: " + str(g))
        
    def load_test(self, group, name, info):
        test = TestInfo(name)
        
        if "variables" in info.keys():
            # TODO: load variables
            pass
        
        group.addTest(test)
        pass
            
        
    @staticmethod
    def load(test_paths : List[str])->'TestspecRegistry':
        """Loads test-config files from the specified directories"""
        ret = TestspecRegistry()
        
        for p in test_paths:
            for f in os.listdir(p):
                ext = os.path.splitext(f)
                if ext[1] == ".json":
                    print("Test file: " + str(os.path.join(p, f)))
                    ret.load_testspec(os.path.join(p, f))
                    
        return ret