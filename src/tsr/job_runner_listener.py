'''
Created on Mar 7, 2020

@author: ballance
'''

class JobRunnerListener(object):
    
    def job_started(self, job):
        pass
    
    def job_finished(self, job):
        pass