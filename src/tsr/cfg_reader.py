'''
Created on Mar 8, 2020

@author: ballance
'''

import configparser
from tsr.messaging import verbose_note

class CfgReader(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def read_cfg(path, info):
        reader = CfgReader()
        reader.read(path, info)
    
    def read(self, path, info):

        config = configparser.ConfigParser()
        config.read(path)

        if config.has_section("tsr"):
            tsr = config["tsr"]
            for key in tsr.keys():
                if key == "project":
                    info.project = tsr["project"]
                elif key == "engine":
                    info.engine = tsr["engine"]
                elif key == "tools":
                    tools = map(lambda s:s.strip(), tsr["tools"].split())
                    for tool in tools:
                        info.add_tool(tool)
        else:
            verbose_note("config file doesn't have a 'tsr' section")
        