'''
Created on Sep 29, 2019

@author: ballance
'''
from vsr.task_base import TaskBase
import subprocess

class TaskMake(TaskBase):
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        subprocess.call(['make'])
        