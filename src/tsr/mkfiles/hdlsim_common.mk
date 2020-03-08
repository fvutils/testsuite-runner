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

ifeq (,$(TSR_VLOG_ARGS))
ifeq (,$(wildcard $(SIM_DIR)/scripts/vlog_$(SIM).f))
TSR_VLOG_ARGS += -f $(SIM_DIR_A)/scripts/vlog.f
else
TSR_VLOG_ARGS += -f $(SIM_DIR_A)/scripts/vlog_$(SIM).f
endif
endif

ifeq (,$(TSR_VCOM_ARGS))
ifneq (,$(wildcard $(SIM_DIR)/scripts/vhdl_$(SIM).f))
TSR_VCOM_ARGS += -f $(SIM_DIR_A)/scripts/vhdl_$(SIM).f
else
ifneq (,$(wildcard $(SIM_DIR)/scripts/vhdl.f))
TSR_VCOM_ARGS += -f $(SIM_DIR_A)/scripts/vhdl.f
endif
endif
endif

else # Rules

hdlsim-plusargs:
	@echo "+TIMEOUT=%t - Specify simulation timeout in units of ps, ns, us, ms, or s"

endif

