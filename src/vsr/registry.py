'''
Created on Sep 29, 2019

@author: ballance
'''

_registry_inst = None

class Registry():
    
    def __init__(self):
        self.flow_m = {}
        self.testset_m = {}
        pass
    
    def register_flow(self, name, T):
        self.flow_m[name] = T
        
    @staticmethod
    def inst():
        global _registry_inst
        if _registry_inst is None:
            _registry_inst = Registry()
        return _registry_inst
    


