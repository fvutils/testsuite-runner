
User-Specified Variables
========================

- TSR_RUNDIR    -- Specifies the rundir to use 

Common
======

- Q               -- Prefix variable used to suppress output (eg $(Q)cmd)

- TSR_PYTHON      -- Path to the Python interpreter used by TSR
- TSR_PYTHONPATH  -- Space-delimited list of python path elements
- TSR_LIBPATH     -- Space-delimited list of LD_LIBRARY_PATH elements
- TSR_PLUSARGS    -- Active plusargs
- TSR_ENGINE      -- Name of the engine being run
- TSR_TOOLS       -- List of currently-enabled tools
- TSR_TESTNAME    -- Name of the running test

- TSR_VERBOSE   -- Display extra information, such as build commands
- TSR_QUIET     -- Suppress all output

- TSR_BUILD_DIR -- Engine-specific directory where build is performed

- TSR_MK_INCLUDES

- TSR_BUILD_PRE_TARGETS
- TSR_BUILD_PRECOMPILE_TARGETS
- TSR_BUILD_COMPILE_TARGETS
- TSR_BUILD_POSTCOMPILE_TARGETS
- TSR_BUILD_POSTBUILD_TARGETS
- TSR_BUILD_PRELINK_TARGETS
- TSR_BUILD_LINK_TARGETS
- TSR_BUILD_POSTLINK_TARGETS
- TSR_BUILD_POST_TARGETS

- TSR_REGRESS_PRE_TARGETS       - Targets run before a regression starts
- TSR_RUN_PRE_TARGETS           - Targets run before each test run
- TSR_RUN_TARGETS               - Targets to run as part of a test run
- TSR_RUN_POST_TARGETS          - Targets to run after each test run
- TSR_REGRESS_POST_TARGETS      - Targets run after a regression completes

- TSR_RUN_ENV_VARS   -- List of VAR=VAL assignments
- TSR_RUN_ENV_VARS_V -- Prefix commands with this

- TSR_RUN_ARGS      -- Arguments to pass to the engine
- TSR_RUN_FLAGS     -- Tool flags to pass to the engine


HDL-Sim Engines
===============
- TSR_HDL_LANGUAGE  -- verilog, systemverilog
-- Note: Do we need to have an HDL_LANGUAGES list?
- TSR_TIMEOUT       -- Simulation time after which to timeout
- TSR_VLOG_ARGS     -- Verilog arguments
- TSR_VCOM_ARGS
# Note: remember VLOG_ARGS_HDL, VLOG_ARGS_HVL
- TSR_VLOG_DEFINES  -- List of Verilog macros to define
- TSR_VLOG_INCDIRS  -- List of include directories
- TSR_VPI_LIBRARIES -- List of PLI/VPI libraries to load
- TSR_DPI_LIBRARIES -- List of DPI libraries to load
- TSR_DPI_LDFLAGS   -- Linker flags used for DPI libraries


Simulator Capabilities
----------------------
- HAVE_HDL_DUMP               -- The simulator can dump to VCD using system tasks
- HAVE_HDL_CLKGEN             -- The simulator can generate clocks with behavioral constructs
- HAVE_HDL_VIRTUAL_INTERFACE
- HAVE_DPI
- 
