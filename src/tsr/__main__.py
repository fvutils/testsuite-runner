'''
Created on Sep 24, 2019

@author: ballance
'''
import os
import sys
from argparse import ArgumentParser
from tsr import messaging
from tsr.registry import Registry

_registry = None

def init_registry():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    _registry = Registry()

    _registry.load_mkfiles_dir(os.path.join(pkg_dir, "mkfiles"))
    
    pass

def build(args, plusargs):
    pass

def runtest(args, plusargs):
    # First, get verbosity taken care of
    messaging.set_verbosity(args.v)
    init_registry()
    pass

def regress(args, plusargs):
    # First, get verbosity taken care of
    messaging.set_verbosity(args.v)
    
    init_registry()
    pass

def config_mkfiles(args, plusargs):
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(os.path.join(pkg_dir, "mkfiles"))

def get_parser():
    parser = ArgumentParser()
    subparser = parser.add_subparsers()
    subparser.required = True
    
    build_cmd = subparser.add_parser("build",
        help="Performs compilation/build")
    build_cmd.set_defaults(func=build)
    build_cmd.add_argument("-v", action="count",
        help="Enables verbose output")
    build_cmd.add_argument("--tool", 
        help="Specifies the tool to target")
    
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
    
    args = parser.parse_args()
    args.func(args, plusargs)

if __name__ == "__main__":
    main()
