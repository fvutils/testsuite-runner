from typing import Dict, List

class TestInfo(object):
    
    def __init__(self, name):
        self.parent = None
        self.name = name
        self.description = ""
        self.append_vars : Dict[str, List[str]] = {}
        self.set_vars : Dict[str, str] = []
        
    def collectVariables(self)->Dict[str, str]:
        # Variables that we need to ignore higher up 
        # in the tree because of a 'set-var'
        blocked_vars = self.set_vars.copy()
        ret = self.set_vars.copy()

        # Note: at the same level, consider 'set' andset_vars
        # 'append' to be complementary
        for k in self.append_vars.keys():
            # Append variables from this level
            if k in ret.keys():
                for v in self.append_vars[k]:
                    ret[k] += " " + v
            else:
                ret[k] = v
            
        p = self.parent
        while p is not None:
            # Apply 'set-vars' first
            for k in p.set_vars.keys():
                if k in blocked_vars:
                    continue
                # Prepend the 'set' value
                if k in ret.keys():
                    ret[k] = p.set_vars[k] + " " + ret[k]
                else:
                    ret[k] = p.set_vars[k]

            # Append 'append-vars' next            
            for k in p.append_vars.keys():
                if k in blocked_vars:
                    continue
                if k in ret.keys():
                    ret[k] = p.append_vars[k] + " " + ret[k]
                else:
                    ret[k] = p.append_vars[k]

            # Update blocked_vars with 'set_vars'
            for k in p.set_vars.keys():
                blocked_vars.add(k)            
            p = p.parent
        
        
        return ret

