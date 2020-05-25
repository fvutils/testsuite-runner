'''
Created on May 23, 2020

@author: ballance
'''
import sys
from typing import Dict, List

class VarInfo(object):
    
    def __init__(self):
        self.set_vars : Dict[str, List[str]] = {}
        self.extend_vars : Dict[str, List[str]] = {}

    def addExtendVars(self, variables):
        for v in variables.keys():
            if v in self.extend_vars.keys():
                if isinstance(variables[v],list):
                    self.extend_vars[v].extend(variables[v]) 
                else:
                    self.extend_vars[v].append(variables[v]) 
            else:
                if isinstance(variables[v],list):
                    self.extend_vars[v] = variables[v].copy() 
                else:
                    self.extend_vars[v] = [variables[v]] 
    
    def addSetVars(self, variables):
        for v in variables.keys():
            if v in self.set_vars.keys():
                raise Exception("Multiple 'set-vars' to variable " + v)
            else:
                if isinstance(variables[v],list):
                    self.set_vars[v] = variables[v].copy() 
                else:
                    self.set_vars[v] = [variables[v]] 
        pass
            
    def addVariables(self, variables):
        """Adds variables from the specified dict"""
        for var in variables.keys():
            value = variables[var]
            if isinstance(value, list):
                for val in value:
                    self.append(var, val)
            else:
                self.append(var, value)
                
    def getEnv(self, env)->Dict[str,str]:
        ret = {}
        for v in self.set_vars:
            ret[v] = " ".join(self.set_vars[v])
        
        for v in self.extend_vars.keys():
            if v in env.keys():
                if v not in ret.keys():
                    # Set vars override environment
                    ret[v] = env[v]
            if v not in ret.keys():
                ret[v] = " ".join(self.extend_vars[v])
            else:
                ret[v] += " " + " ".join(self.extend_vars[v])
                
        return ret
            

    def append(self, var, value):
        if var in self.variables.keys():
            self.variables[var].append(value)
        else:
            self.variables[var] = [value]
        
        
    def extend_pathvar(self, envvar, var, basedir=None):
        """Forms a platform-appropriate path"""
        