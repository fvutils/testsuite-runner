'''
Created on Mar 7, 2020

@author: ballance
'''
import os
import shutil

class JobRunner(object):
    # TODO: we should have a listener
    # - job-start
    # - job-complete (and status)
    # TODO: should delegate running jobs to another interface
    
    def __init__(self, 
            cmd_runner,
            job_l, 
            global_plusargs=None):
        self.cmd_runner = cmd_runner
        self.job_l = job_l
        self.max_par = 1
        self.global_plusargs = global_plusargs
        self.job_listener = None
        
    async def run(self):
        job_idx = 0
        running_jobs = 0
        process_l = []
        seed = 1
        active_jobs = {}
        
        while job_idx < len(self.job_l) or running_jobs > 0:
            
            # Start as many jobs as possible
            while running_jobs < self.cmd_runner.queue_max() and job_idx < len(self.job_l):
                job = self.job_l[job_idx]
                    
                # Clean up behind old run directories
                if os.path.isdir(job.job_rundir):
                    shutil.rmtree(job.job_rundir)
                
                if not os.path.isdir(job.job_rundir):
                    os.makedirs(job.job_rundir)
                    
                # Create a variables file for the Makefile to read
                with open(os.path.join(job.job_rundir, "variables.mk"), "w") as f:
                    f.write("#********************************************************************\n")
                    f.write("#* variables.mk -- Defines variables used for this test\n")
                    f.write("#********************************************************************\n")
                    # TODO: TSR_TESTNAME
#                    f.write("TSR_TESTNAME := %s", job.name)
                    f.write("\n")
                    
                    # TODO: TSR_MK_INCLUDES
                    f.write("\n")
                    f.write("# Test-specific makefiles\n")
                    for mk in job.mk_includes:
                        f.write("TSR_MK_INCLUDES += %s\n" % (mk))
                        
                    # Global plusargs first
                    f.write("\n")
                    f.write("# Global (command-line) plusargs\n")
                    for p in self.global_plusargs:
                        f.write("TSR_PLUSARGS += %s\n" % (p))
                        
                    f.write("\n")
                    f.write("# Test-specific plusargs\n")
                    for p in job.plusargs:
                        f.write("TSR_PLUSARGS += %s\n" % (p))
                
                env = os.environ.copy()
                for v in job.env.keys():
                    env[v] = job.env[v]

                if self.job_listener is not None:
                    self.job_listener.job_started(job)
                await self.cmd_runner.queue(
                    job_idx, 
                    job.cmd, 
                    cwd=job.job_rundir, 
                    env=env)
                running_jobs += 1
                    
#                    seed_str = ("%04d" % (seed))
                    
                job_idx += 1
                
            # Wait for at least one job to complete
            job_results = await self.cmd_runner.wait()
            
            for r in job_results:
                print("result: " + str(r))
                # TODO: result is (id, status)
                # TODO: notify listener that a job is complete
                id = r[0]
                status = r[1]
                job = self.job_l[id]
                
                if self.job_listener is not None:
                    self.job_listener.job_finished(job)

                running_jobs -= 1
                    
