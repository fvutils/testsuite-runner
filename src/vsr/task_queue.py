'''
Created on Sep 29, 2019

@author: ballance
'''
from vsr.task_base import TaskBase

class TaskQueue(TaskBase):
    
    def __init__(self):
        self.task_l = []
        
    def run(self):
        TaskBase.run(self)