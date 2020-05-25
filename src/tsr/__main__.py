'''
Created on Sep 24, 2019

@author: ballance
'''
from argparse import ArgumentParser
import os
import sys

from tsr import messaging
from tsr.cfg_reader import CfgReader
from tsr.messaging import verbose_note, error, note
from tsr.registry import Registry
from tsr.run_ctxt import RunCtxt
from tsr.subprocess_cmd_runner import SubprocessCmdRunner
import asyncio
from tsr.tsr_env import TsrEnv
from test.support.testresult import get_test_runner
import shutil
from tsr.job import Job
from tsr.job_runner import JobRunner
from tsr.filelist_parser import FilelistParser
from tsr.project_config import ProjectConfig
from tsr.testspec_registry import TestspecRegistry
from typing import List
from tsr.test_info import TestInfo


_registry = None
_cmd_runner = None
_env = None

def common_init(args):
    """Performs initialization used by all tasks"""
    global _registry, _cmd_runner, _env
    
    verbosity = 0 if args.v is None else args.v
    messaging.set_verbosity(verbosity)
    
    _registry = Registry.inst()
    _registry.load()
    
    _cmd_runner = SubprocessCmdRunner()
    _env = TsrEnv()
    _env.set_verbose(verbosity > 0)
    
    _env.env["TSR_LAUNCH_DIR"] = os.getcwd()

def expand_var(val, env, project_env):
    ret = val
    
    return ret
        

def build_run_init(args, plusargs):
    """Performs common initialization needed for build and run actions"""
    common_init(args)
    
    ctxt = RunCtxt()
    
    cwd = os.getcwd()
    ctxt.launch_dir = cwd
    
    
    if "TSR_RUNDIR" in os.environ.keys():
        ctxt.rundir = os.environ["TSR_RUNDIR"]
        
    if hasattr(args, "rundir") and args.rundir is not None:
        ctxt.rundir = args.rundir
        
    if ctxt.rundir is None:
        ctxt.rundir = os.path.join(cwd, "rundir")
    
    # Check for characteristics that we recognize
    if not os.path.isfile(os.path.join(cwd, "scripts", "Makefile")):
        raise Exception("scripts/Makefile does not exist")
    
    # Get a default for the project name
    ctxt.project = os.path.basename(os.path.dirname(cwd))
    
    if os.path.join(cwd, "tsr-config.json"):
        verbose_note("Reading project-specific configuration")
        ctxt.project_cfg = ProjectConfig.read(os.path.join(cwd, "tsr-config.json"))
    else:
        raise Exception("No project configuration (tsr-config.json) file present")
    
    project_env = ctxt.project_cfg.getEnv(_env.env)
    print("Project Env")
    for k in project_env.keys():
        print("Var " + k + "=" + project_env[k])
        val = project_env[k]
        if val.find("$") != -1:
            # Expand variable
            val = expand_var(val, _env.env, project_env)
        _env.env[k] = val
    
    ctxt.engine = ctxt.project_cfg.default_engine

    if hasattr(args, "engine") and args.engine is not None:
        ctxt.engine = args.engine

    if ctxt.engine is not None:
        note("Running with engine " + ctxt.engine)
        _env.env["TSR_ENGINE"] = ctxt.engine
        engine_info = _registry.get_engine(ctxt.engine)
        
        if engine_info is None:
            error("No engine named \"" + ctxt.engine + "\" is available")
            note("Available engines:")
            for e in _registry.engines:
                e.load_info()
                print("    " + e.name + " - " + e.description)
            raise Exception("Engine \"" + ctxt.engine + "\" doesn't exist")
        engine_info.load_info()
        ctxt.engine_info = engine_info
    else:
        note("No engine specified")
        _env.env["TSR_ENGINE"] = "none"
  
    ctxt.tools = ctxt.tools.union(ctxt.project_cfg.tools)
    
    # Gather any additional tools from the command-line
    for p in plusargs:
        print("plusarg: " + p)
        if p.startswith("+tool.") and p.find('.', len("+tool.")) == -1:
            tool = p[len("+tool."):]
            print("TOOL: " + tool)
            ctxt.tools.add(tool)
        
    for tool in ctxt.tools:
        verbose_note("Enabling tool \"" + tool + "\"", 1)
        tool_info = _registry.get_tool(tool)
        
        if tool_info is None:
            raise Exception("No tool named \"" + tool + "\"")
        tool_info.load_info()
        ctxt.tool_info.append(tool_info)

    builddir = ctxt.get_builddir()

    # Core environment variables    
    _env.env["TSR_BUILD_DIR"] = builddir
    _env.env["TSR_MK_INCLUDES"] = os.path.join(builddir, "tsr.mk")
    _env.env["TSR_ROOT_MKFILE"] = os.path.join(
        ctxt.launch_dir, "scripts", "Makefile")

    # TODO: support clean?
        
    if not os.path.isdir(builddir):
        os.makedirs(builddir)
        
    # Create a makefile to include that includes all
    # engine and tool mkfiles
    with open(os.path.join(builddir, "tsr.mk"), "w") as f:
        f.write("#********************************************************************\n")
        f.write("#* tsr.mk\n")
        f.write("#********************************************************************\n")
        
        if ctxt.engine_info is not None:
            f.write("include " + ctxt.engine_info.mkfile + "\n")
            
        for info in ctxt.tool_info:
            f.write("include " + info.mkfile + "\n")    
    
    return ctxt

def find_tests(spec)->List[TestInfo]:
    search_path = [
        os.path.join(os.getcwd(), "tests")
        ]

    testfile = None
        
    if os.path.isfile(spec):
        testfile = os.path.abspath(spec)
    else:
        for p in search_path:
            if os.path.isfile(os.path.join(p, spec)):
                testfile = os.path.join(p, spec)
            elif os.path.isfile(os.path.join(p, spec + ".f")):
                testfile = os.path.join(p, spec + ".f")
                
    if testfile is None:
        raise Exception("Failed to find test \"" + spec + "\"")
    
    return testfile

def process_testfile(testfile) -> Job:
    job = Job(testfile)
    p = FilelistParser()
    
    p.parse(testfile, os.getcwd())
    
    for t in p.token_l:
        if t.img[0] == "+":
            job.plusargs.append(t.img)
        else:
            print("Warning: unknown token " + t.img)
    
    return job

async def do_build(ctxt):
    build_env = _env.env.copy()
    
    builddir = ctxt.get_builddir()
            
    
    # Create a plusargs.mk file for build
    with open(os.path.join(builddir, "variables.mk"), "w") as f:
        f.write("TSR_PLUSARGS += +foo=bar\n")
    
    build_cmd = ["make", "-f", 
        os.path.join(ctxt.launch_dir, "scripts", "Makefile"),
        "build"]
    
    await _cmd_runner.queue(
        0, 
        build_cmd, 
        env=build_env,
        cwd=builddir)
    
    result = await _cmd_runner.wait()
    
    if result[0][1] != 0:
        raise Exception("Build Failed")

async def build(args, plusargs):
    global _cmd_runner
    ctxt = build_run_init(args, plusargs)
    
    await do_build(ctxt)

#********************************************************************
#* runtest
#********************************************************************
async def runtest(args, plusargs):
    global _cmd_runner
    
    ctxt = build_run_init(args, plusargs)
    
    # TODO: should allow skipping this    
    await do_build(ctxt)
    
    # Load test specs from specified test directories
    # In the case of unit tests, loading the registry
    # may depend on the build step
    test_rgy = TestspecRegistry.load(ctxt.project_cfg.test_paths)

    # TODO: need name of test
    testname = "test"

    tests = test_rgy.getTests(args.test)
    if len(tests) > 1:
        raise Exception("runtest command can only run a single test")
    
    
    job = Job(tests[0].fullname)
    job.job_rundir = ctxt.get_testdir(tests[0].fullname, 0)
    
    test_vars = tests[0].getVariables()
    job.env = _env.env.copy()

    # TODO: Must pass tool list to run makefiles as well
    job.mk_includes.append(os.path.join(
        ctxt.get_builddir(), "tsr.mk"))
    
    # TODO: process global and test-specific plusargs to identify
    # more makefiles to include
            
    job.cmd.extend(["make", "-f", 
        os.path.join(ctxt.launch_dir, "scripts", "Makefile"),
        "run"])
    
    # TODO: gather global plusargs
    runner = JobRunner(_cmd_runner, [job], plusargs)
    
    await runner.run()

    print("--> wait_job")    
    await _cmd_runner.wait()
    print("<-- wait_job")    
    
async def regress(args, plusargs):
    ctxt = build_run_init(args, plusargs)
    
    pass

def _dump_tests(ind, group):
    if group.name is not None:
        print(ind + group.name)

    for t in group.tests:
        print(ind + "  " + t.name)
        
    for g in group.testgroups:
        _dump_tests(ind + "    ", g)
        

async def list_tests(args, plusargs):
    ctxt = build_run_init(args, plusargs)
    
    # Load test specs from specified test directories
    # In the case of unit tests, loading the registry
    # may depend on the build step
    test_rgy = TestspecRegistry.load(ctxt.project_cfg.test_paths)
    _dump_tests("", test_rgy)
    
    

async def config_mkfiles(args, plusargs):
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(os.path.join(pkg_dir, "mkfiles"))

def get_parser():
    parser = ArgumentParser(prog="tsr")
    subparser = parser.add_subparsers()
    subparser.required = True
    subparser.dest = 'command'
    
    build_cmd = subparser.add_parser("build",
        help="Performs compilation/build")
    build_cmd.set_defaults(func=build)
    build_cmd.add_argument("-v", action="count",
         help="Enables verbose output")
    build_cmd.add_argument("--engine", "-e",
        help="Specifies the engine to target")
    build_cmd.add_argument("--rundir", "-r",
        help="Specifies the run directory")
    
    list_cmd = subparser.add_parser("list",
            help="Lists available tests")
    list_cmd.set_defaults(func=list_tests)
    list_cmd.add_argument("-v", action="count",
        help="Enables verbose output")
    
    runtest_cmd = subparser.add_parser("runtest",
        help="Runs a single test")
    runtest_cmd.set_defaults(func=runtest)
    runtest_cmd.add_argument("-v", action="count",
        help="Enables verbose output")
    runtest_cmd.add_argument("--quiet", "-q", action="store_true",
        help="Runs the tool in 'quiet' mode")
    runtest_cmd.add_argument("--debug", "-d", action="store_true",
        help="Enables running in 'debug' mode. The definition is tool-specific")
    runtest_cmd.add_argument("--interactive", "-i", action="store_true",
        help="Enables running in 'interactive' mode. The definition is tool-specific")
    runtest_cmd.add_argument("--engine", "-e", 
        help="Specifies the engine to run")
    runtest_cmd.add_argument("test",
        help="Specifies the test to run")
    runtest_cmd.add_argument("--rundir", "-r",
        help="Specifies the run directory")
    
    regress_cmd = subparser.add_parser("regress",
        help="Runs a collection of tests")
    regress_cmd.set_defaults(func=regress)
    regress_cmd.add_argument("-v", action="count",
        help="Enables verbose output")
    regress_cmd.add_argument("--debug", "-d", action="store_true",
        help="Enables running in 'debug' mode. The definition is tool-specific")
    regress_cmd.add_argument("--test", "-t", action="append",
        help="Specifies an individual test to run")
    regress_cmd.add_argument("--testlist", "-tl", action="append",
        help="Specifies a testlist to run")
    regress_cmd.add_argument("--engine", "-e",
        help="Specifies the primary engine to run")
    regress_cmd.add_argument("--max_par", "-j",
        help="Specifies the number of jobs to run in parallel")
    regress_cmd.add_argument("--rundir", "-r",
        help="Specifies the run directory")
    
    config_mkfiles_cmd = subparser.add_parser("config-mkfiles",
        help="Provides information about TSR")
    config_mkfiles_cmd.set_defaults(func=config_mkfiles)
    
    return parser
    

def main(args=None):
    if args is None:
        args = sys.argv

    # Remove plusargs first, since these don't go through
    # regular processing
    plusargs = []
    i = 0
    while i < len(args):
        if args[i][0] == "+":
            plusargs.append(args[i])
            del args[i]
        else:
            i += 1
            
    parser = get_parser()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    args = parser.parse_args()
    loop.run_until_complete(args.func(args, plusargs))

if __name__ == "__main__":
    main()
