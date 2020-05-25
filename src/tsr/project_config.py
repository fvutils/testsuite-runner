'''
Created on May 23, 2020

@author: ballance
'''
import json
import os
from typing import Dict, List

from tsr import messaging
from tsr.mkfiles.var_info import VarInfo


class ProjectConfig(VarInfo):
    
    def __init__(self, name):
        VarInfo.__init__(self)
        self.name = name
        self.variables : Dict[str, List[str]] = {}
        self.tools : Set[str] = set()
        self.default_engine = None
        self.supported_engines : Dict[str, object] = {}
        self.test_paths : List[str] = []
    
    @staticmethod
    def read(cfg_file)->'ProjectConfig':
        cfg_keys = set([
            "name", "tools", "extend-vars", "set-vars", "engines"
            ])
        with open(cfg_file, "r") as fp:
            cfg_j = json.load(fp)
            
            for key in cfg_j.keys():
                if key not in cfg_keys:
                    messaging.error("Section " + key + " not legal in project config")
                    messaging.note("Legal sections: " + str(cfg_keys))
                    raise Exception("Section " + key + " not legal in project config")
            
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
                ret.addVariables(cfg_j["variables"])
                
            if "extend-vars" in cfg_j.keys():
                ret.addExtendVars(cfg_j["extend-vars"])
                
            if "set-vars" in cfg_j.keys():
                ret.addSetVars(cfg_j["set-vars"])
            
            if "tests" in cfg_j.keys():
                print("TODO: tests specified")
            else:
                ret.test_paths = [os.path.join(os.getcwd(), "tests")]
                    
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