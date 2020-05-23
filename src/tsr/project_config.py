'''
Created on May 23, 2020

@author: ballance
'''
from typing import Dict, List
import json
from tsr import messaging


class ProjectConfig(object):
    
    def __init__(self, name):
        self.name = name
        self.variables : Dict[str, List[str]] = {}
        self.tools : Set[str] = set()
        self.default_engine = None
        self.supported_engines : Dict[str, object] = {}
        
    
    @staticmethod
    def read(cfg_file)->'ProjectConfig':
        with open(cfg_file, "r") as fp:
            cfg_j = json.load(fp)
            
            if "name" not in cfg_j.keys():
                raise Exception("Project configuration doesn't specify 'name'")
            
            ret = ProjectConfig(cfg_j["name"])
            
            if "tools" in cfg_j.keys():
                if isinstance(cfg_j["tools"], list):
                    for tool in cfg_j["tools"]:
                        print("Add tool: " + str(tool))
                        ret.tools.add(tool)
                else:
                    raise Exception("Expecting 'tools' to be a list")
                
            if "variables" in cfg_j.keys():
                for var in cfg_j["variables"]:
                    print("var: " + str(var))
                    
            if "engines" in cfg_j.keys():
                engines = cfg_j["engines"]
                if "default" in engines.keys():
                    ret.default_engine = engines["default"]
                else:
                    messaging.warn("project configuration does not specify a default engine")
                    
                if "supported" in engines.keys():
                    for eng in engines["supported"]:
                        print("Supported engine: " + eng)
            else:
                messaging.warn("project configuration does not specify engine information")
            
            
        return ret