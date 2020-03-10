#****************************************************************************
#* tsr_hdlsim_common.mk
#*
#* Common include for HDL simulator-type engines 
#*
#* TSR_VLOG_ARGS
#* TSR_VLOG_DEFINES
#* TSR_VLOG_INCDIRS
#* TSR_TB_MODULES
#* TSR_TB_MODULES_HDL
#* TSR_TB_MODULES_HVL
#****************************************************************************

ifneq (1,$(RULES))

ifeq (,$(TSR_VLOG_ARGS_HDL))
ifneq (,$(wildcard $(TSR_LAUNCH_DIR)/scripts/vlog_$(TSR_ENGINE)_hdl.f))
TSR_VLOG_ARGS_HDL += -f $(TSR_LAUNCH_DIR)/scripts/vlog_$(TSR_ENGINE)_hdl.f
else
TSR_VLOG_ARGS_HDL += -f $(TSR_LAUNCH_DIR)/scripts/vlog_hdl.f
endif
endif

ifeq (,$(TSR_VLOG_ARGS))
ifneq (,$(wildcard $(TSR_LAUNCH_DIR)/scripts/vlog_$(TSR_ENGINE)_hdl.f))
TSR_VLOG_ARGS += -f $(TSR_LAUNCH_DIR)/scripts/vlog_$(TSR_ENGINE)_hdl.f
else
TSR_VLOG_ARGS += -f $(TSR_LAUNCH_DIR)/scripts/vlog_$(SIM).f
endif
endif

ifeq (,$(TSR_VCOM_ARGS))
ifneq (,$(wildcard $(TSR_LAUNCH_DIR)/scripts/vhdl_$(SIM).f))
TSR_VCOM_ARGS += -f $(TSR_LAUNCH_DIR)/scripts/vhdl_$(SIM).f
else
ifneq (,$(wildcard $(TSR_LAUNCH_DIR)/scripts/vhdl.f))
TSR_VCOM_ARGS += -f $(TSR_LAUNCH_DIR)/scripts/vhdl.f
endif
endif
endif

TSR_RUN_ARGS += +TESTNAME=$(TESTNAME)

ifeq (true,$(TSR_QUIET))
REDIRECT:= >simx.log 2>&1
else
REDIRECT:=2>&1 | tee simx.log
endif

else # Rules

hdlsim-plusargs:
	@echo "+TIMEOUT=%t - Specify simulation timeout in units of ps, ns, us, ms, or s"

endif

