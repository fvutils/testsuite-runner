'''
Created on Mar 7, 2020

@author: ballance
'''

import os
import sys
import importlib

from tsr.engine_info import EngineInfo
from tsr.messaging import verbose_note, error
from tsr.tool_info import ToolInfo
import subprocess
from _io import StringIO
import cmd
from tsr.plusarg_info import PlusargInfo
from json import tool
import json


class Registry(object):
    
    _inst = None
    
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

    @staticmethod    
    def inst():
        if Registry._inst is None:
            Registry._inst = Registry()
        return Registry._inst
    
    def get_engine(self, name):
        for e in self.engines:
            if e.name == name:
                return e 
            
        return None
    
    def get_tool(self, name):
        for e in self.tools:
            if e.name == name:
                return e 
            
        return None

    def register_engine(self, engine_info):
        self.engines.append(engine_info)    

    def register_tool(self, tool_info):
        self.tools.append(tool_info)
    
    def _process_pythonpath_dir(self, pp_dir):
        for f in os.listdir(pp_dir):
            if f == ".tsr" and os.path.isfile(os.path.join(pp_dir, "__init__.py")):
                # TODO: this is a TSR extension directory
                print("TSR plugin (" + os.path.join(pp_dir, f) + ")")
                import importlib.util
                print("--> load " + pp_dir)
                spec = importlib.util.spec_from_file_location(
                    "vlsim.tsr", 
                    os.path.join(pp_dir, "__init__.py"),
                    submodule_search_locations=None)
                print("<-- load " + pp_dir + " " + str(spec))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)

            elif os.path.splitext(f)[1] == ".egg-link":
                line = None
                with open(os.path.join(pp_dir, f), "r") as f:
                    line = f.readline().strip()

                if line is not None and line != "":
                    print("Process editable package: " + line)
                    self._process_pythonpath_dir(line)                    
            elif not f.startswith("__") and os.path.isdir(os.path.join(pp_dir, f)):
                self._process_pythonpath_dir(os.path.join(pp_dir, f))
        
    
    def load(self, load_info=False):
        for pp in self.pythonpath:
            if os.path.isdir(pp):
                self._process_pythonpath_dir(pp)
        
        for mkfile_dir in self.mkfile_dirs:
            self._load_mkfiles_dir(mkfile_dir)
            
        if load_info:
            for info in self.engines:
                info.load_info()
            for info in self.tools:
                info.load_info()

    
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
                        info.rgy = self
                        self.engines.append(info)
                    elif f.startswith("tool_"):
                        name = basename[len("tool_"):]
                        verbose_note("found tool named \"" + name + "\"")
                        info = ToolInfo(name, os.path.join(dir, f))
                        info.rgy = self
                        self.tools.append(info)
                    else:
                        verbose_note("ignore makefile " + f, 2)

    def _load_info(self, info):
        json_file = os.path.join(
            os.path.dirname(info.mkfile),
            os.path.splitext(os.path.basename(info.mkfile))[0] + ".json")
        
        if os.path.isfile(json_file):
            self._load_info_json(info, json_file)
        
        self._load_mkfile_description(info)
        self._load_mkfile_plusargs(info)
        
    def _load_info_json(self, info, json_file):
        with open(json_file, "r") as fp:
            info = json.load(fp)
            
        pass
                    
    def _run_make(self, args):
        cmd = ["make", "TSR_PYTHON=" + sys.executable]
        cmd.extend(args)
        
        out = subprocess.check_output(cmd)
        return out
        

    def _load_mkfile_description(self, info):
        cmd = ["RULES=1", "-f", info.mkfile, info.name + "-info"]
        
        verbose_note("Querying description for \"" + info.name + "\"")

        try:        
            out = self._run_make(cmd)
            info.description = out.decode().strip()
            verbose_note("  Description: \"" + info.description + "\"")
        except Exception as e:
            error("Failed to load description from " + info.mkfile + "(" + str(e) + ")")
    
    def _load_mkfile_plusargs(self, info):
        cmd = ["RULES=1", "-f", info.mkfile, info.name + "-plusargs"]

        verbose_note("Querying plusargs supported by \"" + info.name + "\"")
        try:        
            out = self._run_make(cmd)
            for line in out.decode().splitlines():
                line = line.strip()
                if line.startswith("+"):
                    if line.find('- '):
                        desc = line[line.find('- ')+1:].strip()
                        line = line[:line.find('- ')]
                    else:
                        desc = ""
                    if line.find("=") != -1:
                        # Plusarg with a value
                        name=line[1:line.find('=')].strip()
                        vtype=line[line.find('=')+1:].strip()
                    else:
                        # Just a plain plusarg
                        name=line[1:]
                        vtype=None
                        
                    verbose_note("Plusargs: name=" + str(name) + " vtype=" + str(vtype) + " desc=" + str(desc))
                    plusarg = PlusargInfo(name, desc, vtype)
                    info.add_plusarg(plusarg)
        except Exception as e:
            error("Failed to load description from " + info.mkfile + "(" + str(e) + ")")
        
        
        pass
    
    
            
        