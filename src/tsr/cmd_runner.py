'''
Created on Mar 7, 2020

@author: ballance
'''

class CmdRunner(object):
    
    def queue_max(self):
        """Returns the maximum number of commands to queue"""
        return 1
    
    async def queue(self, id, cmd, env=None):
        raise NotImplementedError("" + str(type(self)) + "::queue not implemented")
    
    async def wait(self, timeout=-1):
        """Waits for one or more jobs to complete. Returns a list of (id,status) tuples"""
        raise NotImplementedError("" + str(type(self)) + "::wait not implemented")
