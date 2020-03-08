'''
Created on Mar 7, 2020

@author: ballance
'''
import os
from tsr.messaging import verbose_note

class MkfilesDirLoader(object):
    
    def __init__(self, dir):
        self.dir = dir
        self.engines = []
        self.tools = []
        
    def load(self):
        if not os.path.isdir(self.dir):
            raise Exception("Directory \"" + str(self.dir) + "\" does not exist")
        
        verbose_note("Processing mkfiles directory " + self.dir)

        for f in os.listdir(self.dir):
            if os.path.isfile(os.path.join(self.dir, f)):
                ext = os.path.splitext(f)[1]
                print("ext=" + ext)
                
                if f.startswith("engine_") and ext == ".mk":
                    verbose_note("Found engine makefile \"" + f + "\"")
                    name = f[len("engine_"):-3]
                    print("Engine: " + name)
                elif f.startswith("tool_") and ext == ".mk":
                    verbose_note("Found tool makefile \"" + f + "\"")
                    name = f[len("tool_"):-3]
                    print("Tool: " + name)
        
    
        