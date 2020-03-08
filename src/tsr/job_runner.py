'''
Created on Mar 7, 2020

@author: ballance
'''

class JobRunner(object):
    # TODO: we should have a listener
    # - job-start
    # - job-complete (and status)
    # TODO: should delegate running jobs to another interface
    
    def __init__(self, run_root, job_l, global_plusargs=None):
        self.run_root = run_root
        self.job_l = job_l
        self.max_par = 1
        self.global_plusargs = global_plusargs
        self.job_listener = None
        self.cmd_runner = None
        
    async def run(self):
        job_idx = 0
        running_jobs = 0
        process_l = []
        seed = 1
        
        while job_idx < len(self.job_l) or running_jobs > 0:
            
            # Start as many jobs as possible
            while running_jobs < self.cmd_runner.queue_max() and job_idx < len(self.job_l):
                job = self.job_l[job_idx]
                    
                cmd = []
                cwd = None
                env = None
                
                # TODO: maybe each job knows where it 
                # needs to run already?

                if self.job_listener is not None:
                    self.job_listener.job_started(job)
                await self.cmd_runner.queue(job_idx, cmd, cwd, env)
                running_jobs += 1
                    
#                    seed_str = ("%04d" % (seed))
                    
                job_idx += 1
                
            # Wait for at least one job to complete
            job_results = await self.cmd_runner.wait()
            
            for r in job_results:
                # TODO: result is (id, status)
                # TODO: notify listener that a job is complete
                id = r[0]
                status = r[1]
                job = self.job_l[id]
                
                if self.job_listener is not None:
                    self.job_listener.job_finished(job)

                running_jobs -= 1
                    
