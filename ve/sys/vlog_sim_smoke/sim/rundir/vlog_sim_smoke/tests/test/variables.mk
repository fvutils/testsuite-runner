#********************************************************************
#* variables.mk -- Defines variables used for this test
#********************************************************************


# Test-specific makefiles
TSR_MK_INCLUDES += /project/fun/testsuite-runner/testsuite-runner/ve/sys/vlog_sim_smoke/sim/rundir/vlog_sim_smoke/ivl/tsr.mk

# Global (command-line) plusargs
TSR_PLUSARGS += +tool.cocotb

# Test-specific plusargs
TSR_PLUSARGS += +UVM_TESTNAME=bar
TSR_PLUSARGS += +tool=foo
