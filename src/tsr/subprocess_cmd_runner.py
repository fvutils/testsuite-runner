'''
Created on Mar 8, 2020

@author: ballance
'''
from tsr.cmd_runner import CmdRunner
import subprocess
import asyncio

class SubprocessCmdRunner(CmdRunner):
    
    def __init__(self):
        super().__init__()
        self.queue_max = 1
        self.proc_id_map = {}
        self.process_l = []
        
    def queue_max(self):
        return self.queue_max
    
    async def queue(self, id, cmd, env=None, cwd=None):
        process = await asyncio.create_subprocess_exec(
            cmd, env=env, cwd=cwd)
        self.proc_id_map[process] = id
        self.process_l.append(process)
        
    async def wait(self, timeout=-1):
        await self.process_l
        