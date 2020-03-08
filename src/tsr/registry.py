'''
Created on Mar 7, 2020

@author: ballance
'''

import os
import sys

from tsr.engine_info import EngineInfo
from tsr.messaging import verbose_note, error
from tsr.tool_info import ToolInfo
import subprocess
from _io import StringIO
import cmd


class Registry(object):
    
    def __init__(self):
        self.engines = []
        self.tools = []
        # Directories
        self.mkfile_dirs = []
        
        # PYTHONPATH
        self.pythonpath = []
        
        # Add the system mkfiles directory
        self.mkfile_dirs.append(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "mkfiles"))
        
        # Load up the entries in the system path
        self.pythonpath.extend(sys.path)
        
        
        
        pass
    
    def load(self):
        
        for pp in self.pythonpath:
            print("pp=" + pp)
            
        
        for mkfile_dir in self.mkfile_dirs:
            self._load_mkfiles_dir(mkfile_dir)

    
    def _load_mkfiles_dir(self, dir):
        """Processes files from a makefiles directory to find engine and tool files"""
        verbose_note("processing mkfiles directory " + dir)
        
        for f in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, f)):
                basename, ext = os.path.splitext(f)
                
                info = None
                
                if ext == ".mk":
                    if f.startswith("engine_"):
                        name = basename[len("engine_"):]
                        verbose_note("found engine named \"" + name + "\"")
                        info = EngineInfo(name, os.path.join(dir, f))
                        self.engines.append(info)
                    elif f.startswith("tool_"):
                        name = basename[len("tool_"):]
                        verbose_note("found tool named \"" + name + "\"")
                        info = ToolInfo(name, os.path.join(dir, f))
                        self.tools.append(info)
                    else:
                        verbose_note("ignore makefile " + f, 2)

                if info is not None:
                    self._load_mkfile_description(info)
                    self._load_mkfile_plusargs(info)
                    
    def _run_make(self, args):
        cmd = ["make", "TSR_PYTHON=" + sys.executable]
        cmd.extend(args)
        
        out = subprocess.check_output(cmd)
        return out
        

    def _load_mkfile_description(self, info):
        cmd = ["RULES=1", "-f", info.mkfile, info.name + "-info"]

        try:        
            out = self._run_make(cmd)
            print("Info output=" + out.decode())
            info.description = out.decode().strip()
        except Exception as e:
            error("Failed to load description from " + info.mkfile + "(" + str(e) + ")")
        
        pass
    
    def _load_mkfile_plusargs(self, info):
        cmd = ["RULES=1", "-f", info.mkfile, info.name + "-plusargs"]

        try:        
            out = self._run_make(cmd)
            print("Plusargs output=" + out.decode())
            for line in out.decode().splitlines():
                line = line.strip()
                if line.startswith("+"):
                    if line.find("=") != -1:
                        # Plusarg with a value
                    else:
                        # Just a plain plusarg
                    plusarg = 
                print("line=" + line)
        except Exception as e:
            error("Failed to load description from " + info.mkfile + "(" + str(e) + ")")
        
        
        pass
    
    
            
        